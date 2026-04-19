import pygame
import sys
import pandas as pd
from .player import Player
from .ball import Ball
from .goal import Goal
from .menu import Menu, draw_tutorial
from .timer import Timer
from .data_logger import DataLogger

WIDTH = 1280
HEIGHT = 720

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SKE vs CPE")

        self.clock = pygame.time.Clock()

        self.field = pygame.image.load("assets/field.png")
        self.field = pygame.transform.scale(self.field, (WIDTH, HEIGHT))

        ske_head = pygame.image.load("assets/ske_head.png")
        ske_leg = pygame.image.load("assets/ske_leg.png").convert_alpha()

        cpe_head = pygame.image.load("assets/cpe_head.png")
        cpe_leg = pygame.image.load("assets/cpe_leg.png").convert_alpha()

        ske_head = pygame.transform.scale(ske_head, (70, 70))
        cpe_head = pygame.transform.scale(cpe_head, (70, 70))

        leg_width = int(ske_head.get_height() * 0.8)
        leg_height = int(ske_head.get_height() * 0.6)

        ske_leg = pygame.transform.scale(ske_leg, (leg_width, leg_height))
        cpe_leg = pygame.transform.scale(cpe_leg, (leg_width, leg_height))

        self.player1 = Player(200, ske_head, ske_leg, {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "kick": pygame.K_e
        })

        self.player2 = Player(1000, cpe_head, cpe_leg, {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
            "kick": pygame.K_SPACE
        })

        self.ball = Ball()

        self.state = "menu"

        self.logger = DataLogger()

        self.font_big = pygame.font.SysFont("Avenir Next Condensed", 80, bold=True)
        self.font_mid = pygame.font.SysFont("Avenir Next Condensed", 40)
        self.font_score = pygame.font.SysFont("Avenir Next Condensed", 64, bold=True)

        self.menu = Menu(self.screen, self.font_big, self.font_mid)

        self.score_p1 = 0
        self.score_p2 = 0

        self.kicks_p1 = 0
        self.kicks_p2 = 0
        self.jumps_p1 = 0
        self.jumps_p2 = 0

        self.left_goal = Goal(0, 300, 40, 120, "left")
        self.right_goal = Goal(WIDTH - 40, 300, 40, 120, "right")

        self.timer = Timer(60, self.font_mid)

        self.gameover_selected = 0

        self.last_logged_time = -1
        self.prev_kicks = 0
        self.prev_jumps = 0

    def reset_game(self):
        self.score_p1 = 0
        self.score_p2 = 0

        self.player1.x = 200
        self.player1.y = 300

        self.player2.x = 1000
        self.player2.y = 300

        self.ball.reset_position()

        self.timer = Timer(60, self.font_mid)
        self.timer.start_timer()

        self.kicks_p1 = 0
        self.kicks_p2 = 0
        self.jumps_p1 = 0
        self.jumps_p2 = 0

        self.last_logged_time = -1
        self.prev_kicks = 0
        self.prev_jumps = 0

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
                        self.state = "gameplay"
                        self.reset_game()
                        self.menu.start_game = False

                    elif self.menu.show_stats:
                        self.state = "stats"
                        self.menu.show_stats = False

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
                        if event.key == pygame.K_e:
                            self.player1.kick(self.ball)
                            self.kicks_p1 += 1

                        if event.key == pygame.K_SPACE:
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
                                self.state = "gameplay"
                                self.reset_game()
                            else:
                                self.state = "menu"

            self.screen.fill((0, 0, 0))

            if self.state == "menu":
                self.menu.draw()

            elif self.state == "tutorial":
                draw_tutorial(self.screen)

            elif self.state == "stats":
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

                title_font = pygame.font.SysFont("Avenir Next Condensed", 56, bold=True)
                stat_font = pygame.font.SysFont("Avenir Next Condensed", 26, bold=True)
                value_font = pygame.font.SysFont("Avenir Next Condensed", 38, bold=True)
                hint_font = pygame.font.SysFont("Avenir Next Condensed", 22, bold=True)

                title = title_font.render("MATCH STATS", True, (255, 255, 255))
                title_rect = title.get_rect(center=(W // 2, 95))
                self.screen.blit(title, title_rect)

                pygame.draw.rect(
                    self.screen,
                    (255, 210, 0),
                    (W // 2 - 190, 132, 380, 6),
                    border_radius=3
                )

                try:
                    df = pd.read_csv("game_data.csv")

                    avg_speed = round(df["ball_speed"].mean(), 2)
                    max_speed = round(df["ball_speed"].max(), 2)
                    total_kicks = int(df["kicks"].sum())
                    total_jumps = int(df["jumps"].sum())

                    stats = [
                        ("AVG BALL SPEED", avg_speed, (170, 255, 170)),
                        ("MAX BALL SPEED", max_speed, (255, 210, 0)),
                        ("TOTAL KICKS", total_kicks, (85, 170, 255)),
                        ("TOTAL JUMPS", total_jumps, (255, 255, 255)),
                    ]

                except:
                    stats = [
                        ("NO DATA YET", "PLAY FIRST", (255, 210, 0)),
                        ("AVG BALL SPEED", "-", (170, 255, 170)),
                        ("TOTAL KICKS", "-", (85, 170, 255)),
                        ("TOTAL JUMPS", "-", (255, 255, 255)),
                    ]

                card_w = 390
                card_h = 105
                gap_x = 28
                gap_y = 26

                grid_w = card_w * 2 + gap_x
                start_x = W // 2 - grid_w // 2
                start_y = 185

                for i, (label, value, color) in enumerate(stats):
                    col = i % 2
                    row = i // 2

                    x = start_x + col * (card_w + gap_x)
                    y = start_y + row * (card_h + gap_y)

                    card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                    card.fill((5, 35, 10, 220))
                    self.screen.blit(card, (x, y))

                    pygame.draw.rect(self.screen, (80, 160, 80), (x, y, card_w, card_h), 2, border_radius=8)
                    pygame.draw.rect(self.screen, color, (x, y, 7, card_h), border_radius=4)

                    label_text = stat_font.render(label, True, (210, 230, 210))
                    value_text = value_font.render(str(value), True, color)

                    self.screen.blit(label_text, (x + 28, y + 20))
                    self.screen.blit(value_text, (x + 28, y + 58))

                hint = hint_font.render("Press ESC to return to menu", True, (180, 180, 180))
                hint_rect = hint.get_rect(center=(W // 2, 595))
                self.screen.blit(hint, hint_rect)



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

                if self.left_goal.check_goal(self.ball):
                    self.score_p2 += 1
                    self.ball.reset_position()

                if self.right_goal.check_goal(self.ball):
                    self.score_p1 += 1
                    self.ball.reset_position()

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

                left_score = self.font_score.render(str(self.score_p1), True, (255,255,255))
                right_score = self.font_score.render(str(self.score_p2), True, (255,255,255))

                self.screen.blit(left_score, (490, 75))
                self.screen.blit(right_score, (750, 75))

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