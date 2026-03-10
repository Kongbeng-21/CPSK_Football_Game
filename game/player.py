class Player:

    def __init__(self,x,image,controls):

        self.x = x
        self.y = 520
        self.vx = 0
        self.vy = 0

        self.image = image
        self.controls = controls

        self.width = 100
        self.height = 100

    def move(self,keys):

        if keys[self.controls["left"]]:
            self.vx = -5

        elif keys[self.controls["right"]]:
            self.vx = 5

        else:
            self.vx = 0

        if keys[self.controls["jump"]] and self.y >= 520:
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

        if self.y > 520:
            self.y = 520
            self.vy = 0

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))