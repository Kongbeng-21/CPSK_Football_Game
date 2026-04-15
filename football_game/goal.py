import pygame
class Goal:
    def __init__(self, x, y, width, height, side):
        self.rect = pygame.Rect(x, y, width, height)
        self.side = side

    def check_goal(self, ball):
        return self.rect.colliderect(ball.rect)
