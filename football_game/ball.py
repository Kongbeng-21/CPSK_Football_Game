import pygame

WIDTH = 1280
GROUND_Y = 390

ball_img = pygame.image.load("assets/ball.png")
ball_img = pygame.transform.scale(ball_img, (50, 50))

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 150

        self.vx = 0
        self.vy = 0

        self.gravity = 0.5
        self.air_resistance = 0.99
        self.ground_friction = 0.92
        self.bounce = 0.8
        self.wall_bounce = 0.85

        self.radius = 25

        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self):
        self.vy += self.gravity

        self.x += self.vx
        self.y += self.vy

        self.vx *= self.air_resistance
        self.vy *= self.air_resistance

        if self.y >= GROUND_Y - self.radius:
            self.y = GROUND_Y - self.radius
            self.vy *= -self.bounce
            self.vx *= self.ground_friction

            if abs(self.vy) < 1:
                self.vy = 0
            if abs(self.vx) < 0.1:
                self.vx = 0

        if self.x <= 0:
            self.x = 0
            self.vx *= -self.wall_bounce

        if self.x >= WIDTH - 50:
            self.x = WIDTH - 50
            self.vx *= -self.wall_bounce

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(ball_img, (self.x, self.y))

    def reset_position(self):
        self.x = WIDTH // 2
        self.y = 100
        self.vx = 0
        self.vy = 0