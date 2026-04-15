import pygame
import random

WIDTH = 1280
ball_img = pygame.image.load("assets/ball.png")
ball_img = pygame.transform.scale(ball_img,(60,60))

class Ball:
    def __init__(self):
        self.x = WIDTH//2
        self.y = 390
        self.vx = random.choice([-6,6])
        self.vy = -5
        self.rect = pygame.Rect(self.x, self.y, 60, 60)
        self.gravity = 0.6
        self.friction = 0.98

    def update(self):
        self.vy += 0.6
        self.x += self.vx
        self.y += self.vy

        if self.y > 390:
            self.y = 390
            self.vy *= -0.4
            self.vx *= self.friction
            if abs(self.vx) < 0.1:
                self.vx = 0

        if self.y < 0:
            self.y = 0
            self.vy *= -1

        if self.x < 0:
            self.x = 0
            self.vx *= -1

        if self.x > WIDTH - 60:
            self.x = WIDTH - 60
            self.vx *= -1
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        max_speed = 12

        if self.vx > max_speed:
            self.vx = max_speed
        if self.vx < -max_speed:
            self.vx = -max_speed

    def draw(self,screen):
        screen.blit(ball_img,(self.x,self.y))
        
    def reset_position(self):
        self.x = WIDTH // 2
        self.y = 390
        self.vx = random.choice([-6, 6])
        self.vy = -5
        self.rect.x = self.x
        self.rect.y = self.y
