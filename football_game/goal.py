import pygame

class Goal:
    def __init__(self, x, y, width, height, side):
        self.rect = pygame.Rect(x, y, width, height)
        self.side = side

    def check_goal(self, ball):
        ball_center_x = ball.x + ball.radius
        ball_center_y = ball.y + ball.radius

        if self.rect.collidepoint(ball_center_x, ball_center_y):
            return True
        return False