import pygame
class Player:
    def __init__(self,x,image,controls):
        self.x = x
        self.y = 360
        self.vx = 0
        self.vy = 0
        self.image = image
        self.controls = controls
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(self.x, self.y, 120, 120)

    def move(self, keys):
        self.vx = 0
        if keys[self.controls["left"]]:
            self.vx -= 5

        if keys[self.controls["right"]]:
            self.vx += 5

        if keys[self.controls["jump"]] and self.y >= 360:
            self.vy = -15

    def kick(self,ball):
        if abs(self.x-ball.x) < 120:
            if self.x < ball.x:
                ball.vx = 10
            else:
                ball.vx = -10

    def update(self):

        self.vy += 0.8
        self.x += self.vx
        self.y += self.vy

        if self.y > 360:
            self.y = 360
            self.vy = 0

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))