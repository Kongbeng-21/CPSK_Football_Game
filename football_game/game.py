import pygame
import sys
from .player import Player
from .ball import Ball
from .goal import Goal
from .menu import Menu
from .timer import Timer

WIDTH = 1280
HEIGHT = 720

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SKE vs CPE")

        self.clock = pygame.time.Clock()

        self.field = pygame.image.load("assets/field.png")
        self.field = pygame.transform.scale(self.field, (WIDTH, HEIGHT))

        ske_img = pygame.image.load("assets/ske_player.png")
        cpe_img = pygame.image.load("assets/cpe_player.png")

        ske_img = pygame.transform.scale(ske_img, (120, 100))
        cpe_img = pygame.transform.scale(cpe_img, (120, 100))

        self.player1 = Player(200, ske_img, {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "kick": pygame.K_e
        })

        self.player2 = Player(1000, cpe_img, {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
            "kick": pygame.K_SPACE
        })

        self.ball = Ball()

        self.state = "menu"

        self.font_big = pygame.font.SysFont("Arial", 80, bold=True)
        self.font_mid = pygame.font.SysFont("Arial", 40)
        self.font_score = pygame.font.SysFont("Arial", 64, bold=True)

        self.menu = Menu(self.screen, self.font_big, self.font_mid)

        self.score_p1 = 0
        self.score_p2 = 0

        self.left_goal = Goal(0, 420, 40, 120, "left")
        self.right_goal = Goal(WIDTH - 40, 420, 40, 120, "right")

        self.timer = Timer(60, self.font_mid)

        self.gameover_options = ["Restart", "Main Menu"]
        self.gameover_selected = 0

    def reset_game(self):
        self.score_p1 = 0
        self.score_p2 = 0
        self.ball.reset_position()
        self.timer = Timer(60, self.font_mid)
        self.timer.start_timer()
        self.gameover_selected = 0
        
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

                # stats
                elif self.state == "stats":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            self.state = "menu"

                # gameplay
                elif self.state == "gameplay":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            self.player1.kick(self.ball)
                        if event.key == pygame.K_SPACE:
                            self.player2.kick(self.ball)

                # gameover
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

            # menu
            if self.state == "menu":
                self.menu.draw()

            # stats
            elif self.state == "stats":
                text = self.font_big.render("Stats Page", True, (255,255,255))
                back = self.font_mid.render("Press B to go back", True, (200,200,200))

                self.screen.blit(text, (400,250))
                self.screen.blit(back, (430,400))

            # gameplay
            elif self.state == "gameplay":
                self.screen.blit(self.field, (0, 0))

                # timer
                self.timer.update_timer()
                self.timer.draw_timer(self.screen)

                if self.timer.is_time_up():
                    self.state = "game_over"

                keys = pygame.key.get_pressed()

                self.player1.move(keys)
                self.player2.move(keys)

                self.player1.update()
                self.player2.update()

                self.player1.x = max(0, min(self.player1.x, WIDTH - 120))
                self.player2.x = max(0, min(self.player2.x, WIDTH - 120))

                self.player1.rect.x = self.player1.x
                self.player2.rect.x = self.player2.x

                if self.player1.rect.colliderect(self.player2.rect):
                    if self.player1.x < self.player2.x:
                        self.player1.x -= 5
                        self.player2.x += 5
                    else:
                        self.player1.x += 5
                        self.player2.x -= 5

                self.ball.update()

                if self.left_goal.check_goal(self.ball):
                    self.score_p2 += 1
                    self.ball.reset_position()

                if self.right_goal.check_goal(self.ball):
                    self.score_p1 += 1
                    self.ball.reset_position()

                if self.ball.rect.colliderect(self.player1.rect):
                    self.ball.vx = abs(self.ball.vx) + 2

                if self.ball.rect.colliderect(self.player2.rect):
                    self.ball.vx = -abs(self.ball.vx) - 2

                left_score = self.font_score.render(str(self.score_p1), True, (255,255,255))
                right_score = self.font_score.render(str(self.score_p2), True, (255,255,255))

                self.screen.blit(left_score, (400, 50))
                self.screen.blit(right_score, (800, 50))

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

            # gameover
            elif self.state == "game_over":
                if self.score_p1 > self.score_p2:
                    text = "SKE Wins!"
                elif self.score_p2 > self.score_p1:
                    text = "CPE Wins!"
                else:
                    text = "Draw!"

                title = self.font_big.render(text, True, (255,255,255))
                self.screen.blit(title, (400,200))

                for i, option in enumerate(self.gameover_options):
                    color = (255,255,0) if i == self.gameover_selected else (200,200,200)
                    text = self.font_mid.render(option, True, color)

                    rect = text.get_rect(center=(640, 350 + i*60))
                    self.screen.blit(text, rect)

            pygame.display.update()
            self.clock.tick(60)