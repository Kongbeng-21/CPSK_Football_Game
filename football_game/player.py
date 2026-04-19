import pygame
import math

GROUND_Y = 320

class Player:
    def __init__(self, x, head_img, leg_img, controls):
        self.x = x
        self.y = GROUND_Y

        self.head_img = head_img
        self.leg_img = leg_img

        self.vx = 0
        self.vy = 0

        self.gravity = 0.8
        self.jump_power = -15

        self.controls = controls

        self.facing_right = True

        self.kicking = False
        self.kick_timer = 0

        self.head_h = self.head_img.get_height()
        self.leg_h = self.leg_img.get_height()

        self.width = self.head_img.get_width()
        self.height = self.head_h + self.leg_h

        self.radius = self.height // 2

    def move(self, keys):
        self.vx = 0

        if keys[self.controls["left"]]:
            self.vx = -6
            self.facing_right = False

        if keys[self.controls["right"]]:
            self.vx = 6
            self.facing_right = True

        if keys[self.controls["jump"]]:
            if self.y >= GROUND_Y:
                self.vy = self.jump_power

    def update(self):
        self.vy += self.gravity

        self.x += self.vx
        self.y += self.vy
        
        self.x = max(0, self.x)
        self.x = min(1280 - self.width, self.x)

        if self.y > GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0

        if self.kicking:
            self.kick_timer -= 1
            if self.kick_timer <= 0:
                self.kicking = False

    def collide_with_ball(self, ball):
        px = self.x + self.width / 2
        py = self.y + self.head_h + self.leg_h / 2

        bx = ball.x + ball.radius
        by = ball.y + ball.radius

        dx = bx - px
        dy = by - py
        distance = math.sqrt(dx**2 + dy**2)

        min_dist = self.radius + ball.radius

        if distance < min_dist:
            if distance == 0:
                distance = 0.1

            overlap = min_dist - distance

            nx = dx / distance
            ny = dy / distance

            ball.x += nx * overlap
            ball.y += ny * overlap

            ball.vx = nx * 8
            ball.vy = ny * 6
            
    def kick(self, ball):
        self.kicking = True
        self.kick_timer = 10

        px = self.x + self.width / 2
        py = self.y + self.head_h + self.leg_h / 2

        bx = ball.x + ball.radius
        by = ball.y + ball.radius

        dx = bx - px
        dy = by - py
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.radius + ball.radius + 30:
            direction = 1 if self.facing_right else -1
            power = abs(self.vx) + 12

            ball.vx = power * direction
            ball.vy = -12 - abs(self.vx) * 0.3

    def draw(self, screen):
        screen.blit(self.head_img, (self.x, self.y))

        leg_x = self.x + 10
        leg_y = self.y + self.head_img.get_height() - 10

        if self.kicking:
            if self.facing_right:
                leg_x += 25
            else:
                leg_x -= 25
            leg_y -= 10

        screen.blit(self.leg_img, (leg_x, leg_y))
        
    def collide_with_player(self, other):
        px = self.x + self.width / 2
        py = self.y + self.head_h + self.leg_h / 2

        ox = other.x + other.width / 2
        oy = other.y + other.head_h + other.leg_h / 2

        dx = ox - px
        dy = oy - py
        distance = math.sqrt(dx**2 + dy**2)

        min_dist = self.radius + other.radius

        if distance < min_dist:
            if distance == 0:
                distance = 0.1

            overlap = min_dist - distance

            nx = dx / distance
            ny = dy / distance

            self.x -= nx * overlap / 2
            self.y -= ny * overlap / 2

            other.x += nx * overlap / 2
            other.y += ny * overlap / 2

            self.vx = -nx * 3
            other.vx = nx * 3