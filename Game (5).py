# -*- coding: utf-8 -*-
import pygame
import random
import time
import os
current_file = os.path.dirname(__file__)

screenwidth = 700
screenheight = 650

screen = pygame.display.set_mode((screenwidth,screenheight)) 
 
pygame.init()


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y): 
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 0)) 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect) 


class Player(pygame.sprite.Sprite): 
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = spaceship
        self.rect = self.image.get_rect()  
        self.isJumping = False 
        self.rect.center = (400 , 600)
        self.radius = 20
        self.jumpTime = 8
        self.currentTime = -self.jumpTime 
        
    def update(self): 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_d] and self.rect.x+self.rect.width < 800: 
            self.rect.x += 5 
        if keys[pygame.K_a] and self.rect.x > 0: 
            self.rect.x -= 5
        if keys[pygame.K_SPACE]:
            player1.shoot()
        screen.blit(self.image, self.rect)
        if self.isJumping: 
            if self.currentTime <= self.jumpTime: 
                if self.currentTime <= 0: 
                    self.rect.y -= round(self.currentTime ** 2 * 0.5)
                elif self.currentTime > 0: 
                    self.rect.y += round(self.currentTime**2 * 0.5 )
                self.currentTime += 1
            else:
                self.isJumping = False 
                self.currentTime = -self.jumpTime
                
    def shoot(self): 
        bullet = Bullet(self.rect.centerx, self.rect.top) 
        all_sprites.add(bullet)
        bullets.add(bullet)


class Obstacle(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien
        self.rect = self.image.get_rect() 
        self.radius = int(self.rect.width/ 2)
        self.rect.x = random.randrange(screenwidth - self.rect.width - 50)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8) 
        
    def update(self): 
        self.rect.y += self.speedy
        if self.rect.top > screenheight + 10: 
            self.rect.x = random.randrange(screenwidth - self.rect.width - 50)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)
        
class Bullet(pygame.sprite.Sprite): 
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = lazer
        self.rect = self.image.get_rect()
        self.rect.center = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        
    def update(self): 
        self.rect.y -= 3
        if self.rect.bottom < 0: 
            self.kill()
        
        
spaceship = pygame.transform.scale(pygame.image.load(os.path.join(current_file, 'spaceship.png')), (64,64))

background = pygame.image.load(os.path.join(current_file,'space.png'))
backgroundY = 0

alien = pygame.transform.scale(pygame.image.load(os.path.join(current_file, 'enemy.png')), (60,60)) 

lazer = pygame.transform.scale(pygame.image.load(os.path.join(current_file, 'laser.png')), (9 ,37))

all_sprites = pygame.sprite.Group() 
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player1 = Player()
all_sprites.add(player1) 

for i in range(5): 
    o = Obstacle() 
    all_sprites.add(o)
    obstacles.add(o)
    

done = False 
clock = pygame.time.Clock() 
while not done: 
    clock.tick(60)
    rel_y = backgroundY % background.get_rect().height
    screen.blit(background, (0, rel_y - background.get_rect().height))
    if rel_y < screenheight: 
        screen.blit(background, (0, rel_y))
    backgroundY += 1
    if backgroundY > 15: 
        backgroundY += 5 
    elif backgroundY > 30: 
        backgroundY += 10
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: 
                player1.isJumping = True
    shots = pygame.sprite.spritecollide(player1 , obstacles, False, pygame.sprite.collide_circle) 
    if shots: 
        done = True
    hits = pygame.sprite.groupcollide(obstacles, bullets, True, True)
    for hit in hits: 
        o = Obstacle() 
        all_sprites.add(o)
        obstacles.add(o)
    all_sprites.update() 
    all_sprites.draw(screen)
    pygame.display.update()
            
pygame.quit() 
