# -*- coding: utf-8 -*-
import pygame, random, time, os
current_file = os.path.dirname(__file__)

screenwidth = 640
screenheight = 640

screen = pygame.display.set_mode((screenwidth,screenheight)) 
 
pygame.init()

def respawn(): 
    o = Obstacle() 
    all_sprites.add(o)
    obstacles.add(o)

def draw_health_bar(surf,x,y,pct): 
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct /100) * bar_length 
    outline_rect = pygame.Rect(x,y,bar_length,bar_height)
    fill_rect = pygame.Rect(x,y,fill, bar_height) 
    pygame.draw.rect(surf,(0,128,0), fill_rect)
    pygame.draw.rect(surf,(255,255,255), outline_rect,2) 


class Player(pygame.sprite.Sprite): 
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = spaceship
        self.rect = self.image.get_rect()  
        self.isJumping = False 
        self.rect.centerx = screenwidth /2
        self.rect.bottom = screenheight - 20
        self.radius = 20
        self.jumpTime = 8
        self.currentTime = -self.jumpTime 
        self.health = 100
        
        
    def update(self): 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_d] and self.rect.x+self.rect.width < 800: 
            self.rect.x += 5 
        if keys[pygame.K_a] and self.rect.x > 0: 
            self.rect.x -= 5
        screen.blit(self.image, self.rect)
                
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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = lazer
        self.rect = self.image.get_rect()
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

for i in range(4): 
    respawn()

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
            if event.key == pygame.K_SPACE:
                player1.shoot()
            if event.key == pygame.K_w: 
                player1.isJumping = True
                
    shots = pygame.sprite.spritecollide(player1 , obstacles, True, pygame.sprite.collide_circle) 
    for shot in shots:
        player1.health -= 10 
        respawn()
        if player1.health <= 0:  
            done = True
            
    hits = pygame.sprite.groupcollide(obstacles, bullets, True, True)
    for hit in hits: 
       respawn()
    all_sprites.update() 
    all_sprites.draw(screen)
    draw_health_bar(screen,5,5,player1.health)
    pygame.display.update()
    screen.fill((255,255,255))
            
pygame.quit() 
         