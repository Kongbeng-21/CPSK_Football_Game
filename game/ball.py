import pygame
import random

WIDTH = 1280

ball_img = pygame.image.load("assets/ball.png")

class Ball:

    def __init__(self):

        self.x = WIDTH//2
        self.y = 300

        self.vx = random.choice([-6,6])
        self.vy = -5

    def update(self):

        self.vy += 0.6

        self.x += self.vx
        self.y += self.vy

        if self.y > 650:
            self.y = 650
            self.vy *= -0.7

        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1

    def draw(self,screen):

        screen.blit(ball_img,(self.x,self.y))