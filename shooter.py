from pygame import *
import pygame
from random import randint

font.init() #font modülü
font1 = font.Font(None, 80) #fontun dosya uzantısı kullanılabilir
font2 = font.Font(None, 30)
win = font1.render("Kazandın!", True, (255, 255, 255))
lose = font1.render("Kaybettin..", True, (83, 72, 139))

shoot = "fire.png"
player = "ship.png"
space = "spacebg.jpg"
ufo = "ufo.png"

mixer.init()
mixer.music.load("spacemusic.mp3")
mixer.music.play()

score = 0
goal = 10
lost = 0
maxlost = 3

winwidth = 700
winheight = 500
display.set_caption("Shooter")
window = display.set_mode((winwidth, winheight))
background = pygame.transform.scale(image.load(space), (winwidth, winheight))

class Rules(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Spaceship(Rules):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < winwidth - 80:
            self.rect.x += self.speed
    def shoot(self):
        fire = Fire(shoot, self.rect.centerx, self.rect.top, 50, 50, -10)
        shooting.add(fire)

class UFO(Rules):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > winheight:
            self.rect.x = randint(80, winwidth - 80)
            self.rect.y = 0
            lost = lost + 1

class Fire(Rules):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

player = Spaceship(player, 5, winheight - 100, 100, 120, 8)
ufos = sprite.Group()
for i in range(1,6):
    ufo1 = UFO(ufo, randint(80, winwidth- 80), -40, 50, 70, randint(1,2))
    ufos.add(ufo1)

shooting = sprite.Group()
run = True
finish = False

while run:
    for e in event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()
    if not finish:
        window.blit(background, (0 , 0))
        text = font2.render("Score:"+ str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text2 = font2.render("Missed"+ str(lost), 1, (255,255,255))
        window.blit(text2, (10,50))
        player.update()
        shooting.update()
        ufos.update()
        player.reset()
        shooting.draw(window)
        ufos.draw(window)
        collides = sprite.groupcollide(ufos, shooting, True, True)
        for c in collides:
           
            score = score + 1
            ufo1 = UFO(ufo, randint(80, winwidth- 80), -40, 50, 70, randint(1,5))
            ufos.add(ufo1)
      
        if sprite.spritecollide(player, ufos, False) or lost >= maxlost:
            finish = True 
            window.blit(lose, (200, 200))

     
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
        display.update()
    time.delay(50)
