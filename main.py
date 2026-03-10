import pygame
import sys
import random

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SKE vs CPE Soccer")

clock = pygame.time.Clock()

# ---------- LOAD ASSETS ----------

field = pygame.image.load("assets/field.png")
ball_img = pygame.image.load("assets/ball.png")

ske_img = pygame.image.load("assets/ske_player.png")
cpe_img = pygame.image.load("assets/cpe_player.png")

font_big = pygame.font.SysFont("Arial",80)
font_mid = pygame.font.SysFont("Arial",40)

# ---------- GAME STATE ----------

game_state = "menu"

# ---------- PLAYER ----------

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

    def update(self):

        self.vy += 0.8

        self.x += self.vx
        self.y += self.vy

        if self.y > 520:
            self.y = 520
            self.vy = 0

    def draw(self):
        screen.blit(self.image,(self.x,self.y))

# ---------- BALL ----------

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

    def draw(self):
        screen.blit(ball_img,(self.x,self.y))

# ---------- CREATE PLAYERS ----------

player1 = Player(
200,
ske_img,
{
"left":pygame.K_a,
"right":pygame.K_d,
"jump":pygame.K_w,
"kick":pygame.K_e
}
)

player2 = Player(
1000,
cpe_img,
{
"left":pygame.K_LEFT,
"right":pygame.K_RIGHT,
"jump":pygame.K_UP,
"kick":pygame.K_SPACE
}
)

ball = Ball()

# ---------- SCORE ----------

score_ske = 0
score_cpe = 0

# ---------- TIMER ----------

match_time = 60
start_ticks = None

# ---------- COUNTDOWN ----------

countdown = 3
count_start = None

# ---------- GOAL TEXT ----------

goal_timer = 0

# ---------- MAIN LOOP ----------

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":

                if event.key == pygame.K_RETURN:

                    game_state = "countdown"
                    count_start = pygame.time.get_ticks()

            if game_state == "gameplay":

                if event.key == pygame.K_e:

                    if abs(player1.x-ball.x) < 120:
                        ball.vx = 10

                if event.key == pygame.K_SPACE:

                    if abs(player2.x-ball.x) < 120:
                        ball.vx = -10

    screen.fill((0,0,0))

    # ---------- MENU ----------

    if game_state == "menu":

        text = font_big.render("SKE vs CPE",True,(255,255,255))
        screen.blit(text,(450,200))

        start = font_mid.render("PRESS ENTER TO START",True,(255,255,0))
        screen.blit(start,(420,400))

    # ---------- COUNTDOWN ----------

    elif game_state == "countdown":

        screen.blit(field,(0,0))

        seconds = (pygame.time.get_ticks()-count_start)//1000

        if seconds < 3:

            num = 3-seconds

            txt = font_big.render(str(num),True,(255,255,255))
            screen.blit(txt,(620,300))

        else:

            go = font_big.render("GO!",True,(255,255,0))
            screen.blit(go,(600,300))

            if seconds > 3:

                game_state = "gameplay"
                start_ticks = pygame.time.get_ticks()

    # ---------- GAMEPLAY ----------

    elif game_state == "gameplay":

        screen.blit(field,(0,0))

        keys = pygame.key.get_pressed()

        player1.move(keys)
        player2.move(keys)

        player1.update()
        player2.update()

        ball.update()

        player1.draw()
        player2.draw()

        ball.draw()

        # GOAL CHECK

        if ball.x < 50 and ball.y > 500:

            score_cpe += 1
            ball = Ball()
            goal_timer = pygame.time.get_ticks()

        if ball.x > WIDTH-50 and ball.y > 500:

            score_ske += 1
            ball = Ball()
            goal_timer = pygame.time.get_ticks()

        # GOAL TEXT

        if pygame.time.get_ticks()-goal_timer < 1500:

            goal = font_big.render("GOAL !!!",True,(255,0,0))
            screen.blit(goal,(520,200))

        # SCOREBOARD

        score_text = font_mid.render(f"SKE {score_ske} : {score_cpe} CPE",True,(255,255,255))
        screen.blit(score_text,(520,20))

        # TIMER

        seconds = 60 - (pygame.time.get_ticks()-start_ticks)//1000

        timer = font_mid.render(str(seconds),True,(255,255,0))
        screen.blit(timer,(620,70))

        if seconds <= 0:

            game_state = "end"

    # ---------- END ----------

    elif game_state == "end":

        if score_ske > score_cpe:
            winner = "SKE WINS"
        elif score_cpe > score_ske:
            winner = "CPE WINS"
        else:
            winner = "DRAW"

        text = font_big.render(winner,True,(255,255,255))
        screen.blit(text,(480,300))

    pygame.display.update()
    clock.tick(60)