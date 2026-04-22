import pygame
import sys
import pandas as pd
import math
from .player import Player
from .ball import Ball
from .goal import Goal
from .menu import Menu, draw_tutorial
from .timer import Timer
from .data_logger import DataLogger
from .sound_manager import SoundManager
from .skin_manager import SkinManager
from football_game.skin_select import run_skin_select
from football_game.player_skin import SKINS

WIDTH = 1280
HEIGHT = 720

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SKE vs CPE")

        self.clock = pygame.time.Clock()

        self.field = pygame.image.load("assets/field.png")
        self.field = pygame.transform.scale(self.field, (WIDTH, HEIGHT))

        leg_w = 92
        leg_h = 66

        self.sound_manager = SoundManager()

        def _load_skin_imgs(skin_data, flip=False):
            try:
                h = pygame.image.load(skin_data["head"]).convert_alpha()
            except Exception:
                h = pygame.image.load(SKINS[0]["head"]).convert_alpha()
            try:
                l = pygame.image.load(skin_data["leg"]).convert_alpha()
            except Exception:
                l = pygame.image.load(SKINS[0]["leg"]).convert_alpha()
            h = pygame.transform.scale(h, (100, 100))
            l = pygame.transform.scale(l, (leg_w, leg_h))
            if flip:
                h = pygame.transform.flip(h, True, False)
                l = pygame.transform.flip(l, True, False)
            return h, l

        self._load_skin_imgs = _load_skin_imgs
        self._leg_w = leg_w
        self._leg_h = leg_h

        self.skin_p1 = SKINS[0]
        self.skin_p2 = SKINS[1]

        p1_head, p1_leg = _load_skin_imgs(self.skin_p1, flip=False)
        p2_head, p2_leg = _load_skin_imgs(self.skin_p2, flip=True)

        self.player1 = Player(200, p1_head, p1_leg, {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "kick": pygame.K_e
        })

        self.player2 = Player(1000, p2_head, p2_leg, {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
            "kick": pygame.K_SPACE
        })

        self.ball = Ball()
        self.state = "menu"
        self.logger    = DataLogger()
        self.match_id  = self.logger.get_next_match_id() - 1
        self.countdown_start_ticks = 0

        self.font_big   = pygame.font.SysFont("Avenir Next Condensed", 80, bold=True)
        self.font_mid   = pygame.font.SysFont("Avenir Next Condensed", 40)
        self.font_score = pygame.font.SysFont("Avenir Next Condensed", 64, bold=True)

        self.menu = Menu(self.screen, self.font_big, self.font_mid)

        self.score_p1 = 0
        self.score_p2 = 0
        self.kicks_p1 = 0
        self.kicks_p2 = 0
        self.jumps_p1 = 0
        self.jumps_p2 = 0
        self.touches_p1 = 0
        self.touches_p2 = 0
        self.shots_p1   = 0
        self.shots_p2   = 0
        self.prev_touch_p1 = False
        self.prev_touch_p2 = False

        self.left_goal  = Goal(0,           300, 40, 120, "left")
        self.right_goal = Goal(WIDTH - 40,  300, 40, 120, "right")

        self.timer = Timer(60, self.font_mid)

        self.gameover_selected = 0
        self.last_logged_time  = -1
        self.prev_kicks = 0
        self.prev_jumps = 0
    def _apply_skins(self, p1_idx, p2_idx):
        self.skin_p1 = SKINS[p1_idx]
        self.skin_p2 = SKINS[p2_idx]
        self.player1.head_img, self.player1.leg_img = self._load_skin_imgs(self.skin_p1, flip=False)
        self.player2.head_img, self.player2.leg_img = self._load_skin_imgs(self.skin_p2, flip=True)
    def reset_game(self):
        self.match_id += 1
        self.score_p1 = 0
        self.score_p2 = 0

        self.player1.x = 200
        self.player1.y = 300

        self.player2.x = 1000
        self.player2.y = 300

        self.ball.reset_position()

        self.timer = Timer(60, self.font_mid)

        self.kicks_p1 = 0
        self.kicks_p2 = 0
        self.jumps_p1 = 0
        self.jumps_p2 = 0
        
        self.touches_p1 = 0
        self.touches_p2 = 0
        self.shots_p1 = 0
        self.shots_p2 = 0

        self.prev_touch_p1 = False
        self.prev_touch_p2 = False


        self.last_logged_time = -1
        self.prev_kicks = 0
        self.prev_jumps = 0

        # Always re-apply current skins after reset so images are never stale
        self.player1.head_img, self.player1.leg_img = self._load_skin_imgs(self.skin_p1, flip=False)
        self.player2.head_img, self.player2.leg_img = self._load_skin_imgs(self.skin_p2, flip=True)

    def get_distance_to_ball(self, player):
        px = player.x + player.width / 2
        py = player.y + player.height / 2

        bx = self.ball.x + self.ball.radius
        by = self.ball.y + self.ball.radius

        return math.sqrt((bx - px) ** 2 + (by - py) ** 2)

    def is_kick_in_range(self, player):
        return self.get_distance_to_ball(player) < player.radius + self.ball.radius + 30

    def get_possession(self):
        dist_p1 = self.get_distance_to_ball(self.player1)
        dist_p2 = self.get_distance_to_ball(self.player2)

        if dist_p1 < dist_p2:
            return "SKE"
        return "CPE"

    def get_ball_zone(self):
        if self.ball.x < WIDTH / 3:
            return "LEFT"
        elif self.ball.x < WIDTH * 2 / 3:
            return "CENTER"
        return "RIGHT"

    def get_attacking_side(self):
        if self.ball.x < WIDTH * 0.4:
            return "CPE_ATTACK"
        elif self.ball.x > WIDTH * 0.6:
            return "SKE_ATTACK"
        return "NEUTRAL"

    def get_winner_now(self):
        if self.score_p1 > self.score_p2:
            return "SKE"
        elif self.score_p2 > self.score_p1:
            return "CPE"
        return "DRAW"

    def update_touch_stats(self):
        touching_p1 = self.get_distance_to_ball(self.player1) < self.player1.radius + self.ball.radius + 5
        touching_p2 = self.get_distance_to_ball(self.player2) < self.player2.radius + self.ball.radius + 5

        if touching_p1 and not self.prev_touch_p1:
            self.touches_p1 += 1

        if touching_p2 and not self.prev_touch_p2:
            self.touches_p2 += 1

        self.prev_touch_p1 = touching_p1
        self.prev_touch_p2 = touching_p2

    def log_stats_once_per_second(self):
        current_time = self.timer.duration - self.timer.time_left

        if current_time == self.last_logged_time:
            return

        self.last_logged_time = current_time

        ball_speed = round(math.sqrt(self.ball.vx ** 2 + self.ball.vy ** 2), 2)
        score_diff = self.score_p1 - self.score_p2

        self.logger.log([
        self.match_id,
        current_time,
        self.timer.duration,
        ball_speed,
        self.score_p1,
        self.score_p2,
        score_diff,
        self.kicks_p1,
        self.kicks_p2,
        self.jumps_p1,
        self.jumps_p2,
        self.get_possession(),
        self.get_ball_zone(),
        self.get_attacking_side(),
        self.touches_p1,
        self.touches_p2,
        self.shots_p1,
        self.shots_p2,
        self.get_winner_now(),
    ])


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == "menu":
                    self.menu.handle_input(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:
                            self.state = "tutorial"

                    if self.menu.start_game:
                        self.menu.start_game = False
                        skin_p1_idx, skin_p2_idx = run_skin_select(self.screen, self.clock)
                        self._apply_skins(skin_p1_idx, skin_p2_idx)
                        self.reset_game()
                        self.state = "countdown"
                        self.countdown_start_ticks = pygame.time.get_ticks()

                    elif self.menu.show_stats:
                        self.state = "stats"
                        self.menu.show_stats = False
                    
                    elif self.menu.show_tutorial:       
                        self.state = "tutorial"          
                        self.menu.show_tutorial = False 

                elif self.state == "tutorial":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"

                elif self.state == "stats":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"

                elif self.state == "gameplay":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            if self.player1.vy == 0:
                                self.jumps_p1 += 1

                        if event.key == pygame.K_UP:
                            if self.player2.vy == 0:
                                self.jumps_p2 += 1

                        if event.key == pygame.K_e:
                            if self.is_kick_in_range(self.player1):
                                if self.player1.facing_right:
                                    self.shots_p1 += 1
                                self.sound_manager.play_kick()

                            self.player1.kick(self.ball)
                            self.kicks_p1 += 1

                        if event.key == pygame.K_SPACE:
                            if self.is_kick_in_range(self.player2):
                                if not self.player2.facing_right:
                                    self.shots_p2 += 1
                                self.sound_manager.play_kick()

                            self.player2.kick(self.ball)
                            self.kicks_p2 += 1


                elif self.state == "game_over":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.gameover_selected = (self.gameover_selected - 1) % 2
                        elif event.key == pygame.K_DOWN:
                            self.gameover_selected = (self.gameover_selected + 1) % 2
                        elif event.key == pygame.K_RETURN:
                            if self.gameover_selected == 0:
                                self.reset_game()
                                self.state = "countdown"
                                self.countdown_start_ticks = pygame.time.get_ticks()
                            else:
                                self.state = "menu"

            self.screen.fill((0, 0, 0))

            if self.state == "menu":
                self.menu.draw()

            elif self.state == "tutorial":
                draw_tutorial(self.screen)

            elif self.state == "stats":
                W, H = self.screen.get_size()
                cx = W // 2
                lx = W // 4
                rx = W * 3 // 4

                stripe_w = 70
                for i in range(W // stripe_w + 2):
                    c = (32, 108, 32) if i % 2 == 0 else (26, 90, 26)
                    pygame.draw.rect(self.screen, c, (i * stripe_w, 0, stripe_w, H))

                field_surf = pygame.Surface((W, H), pygame.SRCALPHA)
                s_lc = (255, 255, 255, 40)
                pygame.draw.rect(field_surf, s_lc, (60, 60, W - 120, H - 120), 2)
                pygame.draw.line(field_surf, s_lc, (cx, 60), (cx, H - 60), 2)
                pygame.draw.circle(field_surf, s_lc, (cx, H // 2), 90, 2)
                self.screen.blit(field_surf, (0, 0))

                overlay = pygame.Surface((W, H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 125))
                self.screen.blit(overlay, (0, 0))

                title_font  = pygame.font.SysFont("Avenir Next Condensed", 54, bold=True)
                team_font   = pygame.font.SysFont("Avenir Next Condensed", 32, bold=True)
                label_font  = pygame.font.SysFont("Avenir Next Condensed", 19, bold=True)
                value_font  = pygame.font.SysFont("Avenir Next Condensed", 40, bold=True)
                record_font = pygame.font.SysFont("Avenir Next Condensed", 36, bold=True)
                hint_font   = pygame.font.SysFont("Avenir Next Condensed", 20, bold=True)

                title = title_font.render("MATCH STATS", True, (255, 255, 255))
                self.screen.blit(title, title.get_rect(center=(cx, 62)))
                pygame.draw.rect(self.screen, (255, 210, 0), (cx - 170, 94, 340, 4), border_radius=2)

                try:
                    df = pd.read_csv("game_data.csv")
                    for _col in ["score_p1", "score_p2", "kicks_p1", "kicks_p2",
                                 "shots_p1", "shots_p2", "possession"]:
                        df[_col] = pd.to_numeric(df[_col], errors="coerce")
                    last = df.groupby("match_id").last().reset_index()
                    matches_played = len(last)
                    ske_wins = int((last["score_p1"] > last["score_p2"]).sum())
                    draws    = int((last["score_p1"] == last["score_p2"]).sum())
                    cpe_wins = int((last["score_p1"] < last["score_p2"]).sum())
                    ske_wr   = round(ske_wins / matches_played * 100) if matches_played else 0
                    cpe_wr   = round(cpe_wins / matches_played * 100) if matches_played else 0
                    g1       = int(last["score_p1"].sum())
                    g2       = int(last["score_p2"].sum())
                    avg_poss = round(df["possession"].mean(), 1)
                    tk1 = int(last["kicks_p1"].sum())
                    tk2 = int(last["kicks_p2"].sum())
                    ts1 = int(last["shots_p1"].sum())
                    ts2 = int(last["shots_p2"].sum())
                    acc1 = round(ts1 / tk1 * 100) if tk1 else 0
                    acc2 = round(ts2 / tk2 * 100) if tk2 else 0
                    no_data = False
                except Exception:
                    matches_played = ske_wins = draws = cpe_wins = 0
                    ske_wr = cpe_wr = g1 = g2 = acc1 = acc2 = 0
                    avg_poss = 50.0
                    no_data = True

                mp_w, mp_h = 260, 64
                mp_x, mp_y = cx - mp_w // 2, 108
                mp_card = pygame.Surface((mp_w, mp_h), pygame.SRCALPHA)
                mp_card.fill((5, 35, 10, 210))
                self.screen.blit(mp_card, (mp_x, mp_y))
                pygame.draw.rect(self.screen, (80, 160, 80), (mp_x, mp_y, mp_w, mp_h), 2, border_radius=6)
                mp_lbl = label_font.render("MATCHES PLAYED", True, (180, 220, 180))
                mp_val = value_font.render(str(matches_played), True, (255, 210, 0))
                self.screen.blit(mp_lbl, mp_lbl.get_rect(center=(cx, mp_y + 18)))
                self.screen.blit(mp_val, mp_val.get_rect(center=(cx, mp_y + 47)))

                th_y = 192
                ske_surf = team_font.render("SKE", True, (255, 210, 0))
                cpe_surf = team_font.render("CPE", True, (100, 190, 255))
                self.screen.blit(ske_surf, ske_surf.get_rect(center=(lx, th_y)))
                self.screen.blit(cpe_surf, cpe_surf.get_rect(center=(rx, th_y)))

                div_top = th_y + 22
                div_bot = H - 52
                pygame.draw.line(self.screen, (70, 130, 70), (cx, div_top), (cx, div_bot), 1)
                pygame.draw.line(self.screen, (60, 110, 60), (110, div_top), (W - 110, div_top), 1)

                SKE_Y = (255, 210,   0)
                CPE_B = (100, 190, 255)
                GRN   = (170, 255, 170)
                PUR   = (200, 160, 255)
                ORG   = (255, 180,  80)

                comp_rows = [
                    ("WIN RATE",       f"{ske_wr}%",          f"{cpe_wr}%",          GRN, GRN),
                    ("TOTAL GOALS",    str(g1),               str(g2),               SKE_Y, CPE_B),
                    ("AVG POSSESSION", f"{avg_poss}%",        f"{round(100-avg_poss,1)}%", PUR, PUR),
                    ("SHOT ACCURACY",  f"{acc1}%",            f"{acc2}%",            ORG, ORG),
                ] if not no_data else [
                    ("WIN RATE",       "–", "–", GRN, GRN),
                    ("TOTAL GOALS",    "–", "–", SKE_Y, CPE_B),
                    ("AVG POSSESSION", "–", "–", PUR, PUR),
                    ("SHOT ACCURACY",  "–", "–", ORG, ORG),
                ]

                row_y0  = 222
                row_gap = 74

                for i, (lbl, sv, cv, sc, cc) in enumerate(comp_rows):
                    ry = row_y0 + i * row_gap
                    if i > 0:
                        pygame.draw.line(self.screen, (55, 105, 55), (110, ry - 8), (W - 110, ry - 8), 1)

                    lbl_surf = label_font.render(lbl, True, (170, 215, 170))
                    self.screen.blit(lbl_surf, lbl_surf.get_rect(center=(cx, ry + 6)))

                    sv_surf = value_font.render(sv, True, sc)
                    cv_surf = value_font.render(cv, True, cc)
                    self.screen.blit(sv_surf, sv_surf.get_rect(center=(lx, ry + 38)))
                    self.screen.blit(cv_surf, cv_surf.get_rect(center=(rx, ry + 38)))

                wr_y = row_y0 + 4 * row_gap
                pygame.draw.line(self.screen, (55, 105, 55), (110, wr_y - 8), (W - 110, wr_y - 8), 1)

                wr_lbl = label_font.render("WIN RECORD", True, (170, 215, 170))
                self.screen.blit(wr_lbl, wr_lbl.get_rect(center=(cx, wr_y + 6)))

                if not no_data:
                    w_ske = record_font.render(f"{ske_wins}W", True, (255, 210,   0))
                    w_d   = record_font.render(f"{draws}D",    True, (210, 210, 210))
                    w_cpe = record_font.render(f"{cpe_wins}W", True, (100, 190, 255))
                    dot_l = record_font.render("·", True, (130, 130, 130))
                    dot_r = record_font.render("·", True, (130, 130, 130))
                    self.screen.blit(w_ske, w_ske.get_rect(center=(lx,      wr_y + 40)))
                    self.screen.blit(dot_l, dot_l.get_rect(center=(cx - 70, wr_y + 40)))
                    self.screen.blit(w_d,   w_d.get_rect(  center=(cx,      wr_y + 40)))
                    self.screen.blit(dot_r, dot_r.get_rect(center=(cx + 70, wr_y + 40)))
                    self.screen.blit(w_cpe, w_cpe.get_rect(center=(rx,      wr_y + 40)))

                hint = hint_font.render("Press ESC to return to menu", True, (160, 160, 160))
                self.screen.blit(hint, hint.get_rect(center=(cx, H - 26)))



            elif self.state == "countdown":
                self.screen.blit(self.field, (0, 0))

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

                elapsed = (pygame.time.get_ticks() - self.countdown_start_ticks) // 1000

                if elapsed >= 4:
                    self.state = "gameplay"
                    self.timer.start_timer()
                else:
                    if elapsed == 3:
                        cd_text = "GO!"
                        cd_color = (80, 255, 80)
                    else:
                        cd_text = str(3 - elapsed)
                        cd_color = (255, 255, 255)

                    font_cd = pygame.font.SysFont("Avenir Next Condensed", 180, bold=True)

                    shadow = font_cd.render(cd_text, True, (0, 0, 0))
                    shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 4, HEIGHT // 2 + 4))
                    self.screen.blit(shadow, shadow_rect)

                    text = font_cd.render(cd_text, True, cd_color)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    self.screen.blit(text, text_rect)

            elif self.state == "gameplay":
                self.screen.blit(self.field, (0, 0))

                self.timer.update_timer()
                self.timer.draw_timer(self.screen)

                if self.timer.is_time_up():
                    self.state = "game_over"

                keys = pygame.key.get_pressed()

                self.player1.move(keys)
                self.player2.move(keys)

                self.player1.update()
                self.player2.update()

                self.ball.update()

                self.player1.collide_with_player(self.player2)
                self.player1.collide_with_ball(self.ball)
                self.player2.collide_with_ball(self.ball)
                self.update_touch_stats()
                self.log_stats_once_per_second()


                if self.left_goal.check_goal(self.ball):
                    self.score_p2 += 1
                    self.ball.reset_position()
                    self.sound_manager.play_goal()

                if self.right_goal.check_goal(self.ball):
                    self.score_p1 += 1
                    self.ball.reset_position()
                    self.sound_manager.play_goal()

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

                left_score = self.font_score.render(str(self.score_p1), True, (255,255,255))
                right_score = self.font_score.render(str(self.score_p2), True, (255,255,255))

                self.screen.blit(left_score, (490, 62))
                self.screen.blit(right_score, (750, 62))

            elif self.state == "game_over":
                W, H = self.screen.get_size()

                stripe_w = 80
                for i in range(W // stripe_w + 1):
                    c = (34, 110, 34) if i % 2 == 0 else (28, 95, 28)
                    pygame.draw.rect(self.screen, c, (i * stripe_w, 0, stripe_w, H))

                line_color = (210, 230, 210)
                pygame.draw.line(self.screen, line_color, (W // 2, 0), (W // 2, H), 2)
                pygame.draw.circle(self.screen, line_color, (W // 2, H // 2), 110, 2)

                overlay = pygame.Surface((W, H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 130))
                self.screen.blit(overlay, (0, 0))

                title_font = pygame.font.SysFont("Arial Black", 62, bold=True)
                winner_font = pygame.font.SysFont("Arial Black", 76, bold=True)
                score_font = pygame.font.SysFont("Arial Black", 56, bold=True)
                option_font = pygame.font.SysFont("Arial", 34, bold=True)
                hint_font = pygame.font.SysFont("Arial", 20, bold=True)

                if self.score_p1 > self.score_p2:
                    result_text = "SKE WINS"
                    result_color = (255, 210, 0)
                elif self.score_p2 > self.score_p1:
                    result_text = "CPE WINS"
                    result_color = (85, 170, 255)
                else:
                    result_text = "DRAW"
                    result_color = (255, 255, 255)

                title = title_font.render("FULL TIME", True, (255, 255, 255))
                title_rect = title.get_rect(center=(W // 2, 95))
                self.screen.blit(title, title_rect)

                pygame.draw.rect(
                    self.screen,
                    (255, 210, 0),
                    (W // 2 - 170, 132, 340, 6),
                    border_radius=3
                )

                result = winner_font.render(result_text, True, result_color)
                result_rect = result.get_rect(center=(W // 2, 220))
                self.screen.blit(result, result_rect)

                score_text = score_font.render(
                    f"{self.score_p1}  -  {self.score_p2}",
                    True,
                    (255, 255, 255)
                )
                score_rect = score_text.get_rect(center=(W // 2, 305))
                self.screen.blit(score_text, score_rect)

                labels = ["PLAY AGAIN", "MAIN MENU"]
                btn_w = 360
                btn_h = 56
                start_y = 390
                gap = 18

                for i, label in enumerate(labels):
                    x = W // 2 - btn_w // 2
                    y = start_y + i * (btn_h + gap)
                    rect = pygame.Rect(x, y, btn_w, btn_h)

                    if i == self.gameover_selected:
                        pygame.draw.rect(self.screen, (255, 210, 0), rect, border_radius=8)
                        text_color = (15, 15, 15)

                        arrow_x = x - 34
                        arrow_y = y + btn_h // 2
                        pygame.draw.polygon(
                            self.screen,
                            (255, 210, 0),
                            [(arrow_x, arrow_y - 10), (arrow_x + 18, arrow_y), (arrow_x, arrow_y + 10)]
                        )
                    else:
                        card = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
                        card.fill((0, 0, 0, 135))
                        self.screen.blit(card, rect.topleft)
                        pygame.draw.rect(self.screen, (160, 160, 160), rect, 2, border_radius=8)
                        text_color = (220, 220, 220)

                    option_text = option_font.render(label, True, text_color)
                    option_rect = option_text.get_rect(center=rect.center)
                    self.screen.blit(option_text, option_rect)

                hint = hint_font.render("UP / DOWN to select    ENTER to confirm", True, (170, 190, 170))
                hint_rect = hint.get_rect(center=(W // 2, 610))
                self.screen.blit(hint, hint_rect)


            pygame.display.update()
            self.clock.tick(60)