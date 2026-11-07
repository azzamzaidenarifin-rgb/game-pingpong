from pygame import *

init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
           self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.original_image = self.image  
        self.angle = 0                    
        self.spin_direction = 1       

    def update_rotation(self):
        self.angle += 5 * self.spin_direction 
        if self.angle >= 360:
            self.angle = 0
        elif self.angle < 0:
            self.angle = 360
        
        self.image = transform.rotate(self.original_image, self.angle)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def change_spin(self):
        self.spin_direction *= -1

back = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")

game = True
finish = False
clock = time.Clock()
FPS = 60

racket1 = Player("racket.png", 30, 175, 4, 50, 150)
racket2 = Player("racket.png", 520, 175, 4, 50, 150)
ball = Ball("ball.png", 270, 220, 4, 60, 60)

game_font = font.SysFont("arial", 40)

score1 = 0
score2 = 0

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        
        racket1.update_1()
        racket2.update_r()
        
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        ball.update_rotation()

        if sprite.collide_rect(racket1, ball):
            speed_x = abs(speed_x) * 1.03
            speed_y *= 1.05
            ball.change_spin()

        elif sprite.collide_rect(racket2, ball):
            speed_x = -abs(speed_x) * 1.03
            speed_y *= 1.03
            ball.change_spin()


        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
            speed_y *= -1
            ball.change_spin()

        if ball.rect.x < -20:
            score2 += 1
            ball.rect.x = 270
            ball.rect.y = 220
            speed_x = 3
            speed_y = 3

        if ball.rect.x > win_width:
            score1 += 1
            ball.rect.x = 270
            ball.rect.y = 220
            speed_x = -3
            speed_y = 3

        racket1.reset()
        racket2.reset()
        ball.reset()

    score1_render = game_font.render(f"P1: {score1}", True, (0, 0, 0))
    score2_render = game_font.render(f"P2: {score2}", True, (0, 0, 0))
    
    window.blit(score1_render, (50, 20))
    window.blit(score2_render, (450, 20))

    display.update()
    clock.tick(FPS)

quit()
