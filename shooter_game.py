from pygame import *
from random import randint
from time import time as timer

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "UFO.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
win_wight = 700
win_height = 500
display.set_caption("Схоотер")
window = display.set_mode((win_wight,win_height))
background = transform.scale(image.load(img_back), (win_wight,win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()

font1 = font.Font(None, 70)
win = font1.render("ты пабэдил!", True, (255, 215, 0))
lose = font1.render("*__*", True, (180, 0, 0))
font2 = font.Font(None, 36)
goal = 15
max_lost = 15
life =3
score = 0
lost = 0


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 11, 15, -45)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
         self.rect.y += self.speed
         global lost
         if self.rect.y > win_height:
             self.rect.x = randint(80, win_wight - 80)
             self.rect.y = 0
             lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -10:
            self.kill()

class Enemy_ast(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
             self.rect.x = randint(80, win_wight - 80)
             self.rect.y = 0

ship = Player(img_hero, 5, win_height - 150, 60, 150, 17.5)

clock = time.Clock()
FPS = 120

monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_wight - 80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(15):
    asteroid = Enemy_ast(img_ast, randint(5, win_wight - 5), -40, 50, 65, randint(10,10))
    asteroids.add(asteroid)


finish = False
run = True
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and rel_time == False:
                    num_fire = num_fire +1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 15 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                    

    if not finish:
        window.blit(background, (0,0))

        text = font2.render("KILS:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0,250,0)

        if life == 2:
            life_color = (250,250,0)

        if life == 1:
            life_color = (250,0,0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < randint(5, 15):
                reload = font2.render("i need bulet", 1, (255,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_wight - 80), -40, 80, 50, randint(1, 7))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            sprite.spritecollide(ship, monsters, True)
            life = life -1

        

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
            
        
                



        display.update()
        clock.tick(FPS)
        

    time.delay(50)


