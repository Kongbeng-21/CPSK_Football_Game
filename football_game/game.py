import pygame
import sys
from .player import Player
from .ball import Ball
from .goal import Goal
from .menu import Menu

WIDTH = 1280
HEIGHT = 720

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("SKE vs CPE Soccer")

        self.clock = pygame.time.Clock()

        self.field = pygame.image.load("assets/field.png")
        self.field = pygame.transform.scale(self.field,(WIDTH,HEIGHT))

        ske_img = pygame.image.load("assets/ske_player.png")
        cpe_img = pygame.image.load("assets/cpe_player.png")

        ske_img = pygame.transform.scale(ske_img,(120,120))
        cpe_img = pygame.transform.scale(cpe_img,(120,120))

        self.player1 = Player(200,ske_img,{
            "left":pygame.K_a,
            "right":pygame.K_d,
            "jump":pygame.K_w,
            "kick":pygame.K_e
        })

        self.player2 = Player(1000,cpe_img,{
            "left":pygame.K_LEFT,
            "right":pygame.K_RIGHT,
            "jump":pygame.K_UP,
            "kick":pygame.K_SPACE
        })

        self.ball = Ball()

        self.state = "menu"

        self.font_big = pygame.font.SysFont("Arial",80)
        self.font_mid = pygame.font.SysFont("Arial",40)

        self.menu = Menu(self.screen,self.font_big,self.font_mid)

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
                if self.state == "gameplay":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            self.player1.kick(self.ball)
                        if event.key == pygame.K_SPACE:
                            self.player2.kick(self.ball)
            self.screen.fill((0,0,0))

            if self.state == "menu":
                self.menu.draw()

            elif self.state == "gameplay":
                self.screen.blit(self.field,(0,0))
                keys = pygame.key.get_pressed()
                self.player1.move(keys)
                self.player2.move(keys)

                self.player1.update()
                self.player2.update()

                self.ball.update()

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)