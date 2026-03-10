import pygame

class Menu:
    def __init__(self,screen,font_big,font_mid):
        self.screen = screen
        self.font_big = font_big
        self.font_mid = font_mid
        self.start_game = False

    def handle_input(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_game = True

    def draw(self):
        title = self.font_big.render("SKE vs CPE",True,(255,255,255))
        self.screen.blit(title,(450,200))

        start = self.font_mid.render("PRESS ENTER TO START",True,(255,255,0))
        self.screen.blit(start,(420,400))