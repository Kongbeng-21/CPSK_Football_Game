import pygame
import sys
import pandas as pd
from .player import Player
from .ball import Ball
from .goal import Goal
from .menu import Menu
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

        head_h = ske_head.get_height()
        
        ske_head = pygame.transform.scale(ske_head, (70, 70))
        cpe_head = pygame.transform.scale(cpe_head, (70, 70))
        
        leg_width = int(head_h * 0.8)
        leg_height = int(head_h * 0.6)

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

        self.font_big = pygame.font.SysFont("Arial", 80, bold=True)
        self.font_mid = pygame.font.SysFont("Arial", 40)
        self.font_score = pygame.font.SysFont("Arial", 64, bold=True)

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

        self.gameover_options = ["Restart", "Main Menu"]
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

                    if self.menu.start_game:
                        self.state = "gameplay"
                        self.reset_game()
                        self.menu.start_game = False

                    elif self.menu.show_stats:
                        self.state = "stats"
                        self.menu.show_stats = False

                elif self.state == "stats":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
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

            elif self.state == "stats":
                self.screen.fill((0,0,0))
                try:
                    df = pd.read_csv("game_data.csv")

                    avg_speed = round(df["ball_speed"].mean(), 2)
                    max_speed = round(df["ball_speed"].max(), 2)
                    total_kicks = int(df["kicks"].sum())
                    total_jumps = int(df["jumps"].sum())

                    title = self.font_big.render("GAME STATS", True, (255,255,255))

                    t1 = self.font_mid.render(f"Avg Ball Speed: {avg_speed}", True, (255,255,255))
                    t2 = self.font_mid.render(f"Max Ball Speed: {max_speed}", True, (255,255,255))
                    t3 = self.font_mid.render(f"Total Kicks: {total_kicks}", True, (255,255,255))
                    t4 = self.font_mid.render(f"Total Jumps: {total_jumps}", True, (255,255,255))

                except:
                    title = self.font_big.render("NO DATA YET", True, (255,255,255))
                    t1 = self.font_mid.render("Play a game first!", True, (200,200,200))
                    t2 = self.font_mid.render("", True, (200,200,200))
                    t3 = self.font_mid.render("", True, (200,200,200))
                    t4 = self.font_mid.render("", True, (200,200,200))

                self.screen.blit(title, (400,150))
                self.screen.blit(t1, (400,280))
                self.screen.blit(t2, (400,340))
                self.screen.blit(t3, (400,400))
                self.screen.blit(t4, (400,460))

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

                self.screen.blit(left_score, (400, 50))
                self.screen.blit(right_score, (800, 50))

                current_time = self.timer.time_left

                if current_time != self.last_logged_time:
                    self.last_logged_time = current_time

                    total_kicks = self.kicks_p1 + self.kicks_p2
                    total_jumps = self.jumps_p1 + self.jumps_p2

                    kicks_this_sec = total_kicks - self.prev_kicks
                    jumps_this_sec = total_jumps - self.prev_jumps

                    self.prev_kicks = total_kicks
                    self.prev_jumps = total_jumps

                    self.logger.log(
                        current_time,
                        abs(self.ball.vx),
                        self.score_p1 - self.score_p2,
                        kicks_this_sec,
                        jumps_this_sec
                    )

            elif self.state == "game_over":
                text = "Draw!"
                if self.score_p1 > self.score_p2:
                    text = "SKE Wins!"
                elif self.score_p2 > self.score_p1:
                    text = "CPE Wins!"

                title = self.font_big.render(text, True, (255,255,255))
                self.screen.blit(title, (400,200))

            pygame.display.update()
            self.clock.tick(60)