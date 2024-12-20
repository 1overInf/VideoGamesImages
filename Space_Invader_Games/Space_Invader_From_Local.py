#To Do: add restart button
from os import path

import pygame
from pygame.locals import *
import random

pygame.init()

#Define fps
clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invade')


#define fonts
font30 = pygame.font.SysFont('Bauhaus 93', 30)
font40 = pygame.font.SysFont('Bauhaus 93', 40)


#Define game variable
#Displays the aliens in a matrix (x, y) or (rows, cols)
rows = 5
cols = 5
#IMPORTANT - Control
alien_cooldown = 500 #bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()

countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 #0 is no game over, 1 means player has won, -1 means player has lost

#Define Color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#Load background image
bg = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/space.png').convert_alpha()

#Function for drawing background
def draw_bg():
    #SCALES BACKGROUND TO FIT SCREEN WIDTH AND HEIGHT
    scaled_bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #DISPLAYS SCALED BG
    screen.blit(scaled_bg, (0, 0))



#define function for creating text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



#CREATE SPACESHIP CLASS
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        #Import spaceship image
        spaceshipp = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/spaceship.png')
        #Scale spaceship image
        self.image = pygame.transform.scale(spaceshipp, (60, 60))
        #self.image = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
    def update(self):
        #Set movement speed
        speed = 8
        #set a cooldown variable
        cooldown = 500 #milliseconds
        game_over = 0
        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed
        #Record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now


        #update mask
        self.mask = pygame.mask.from_surface(self.image)


        #Draw health bar
        pygame.draw.rect(screen, RED, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, GREEN, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            #Explopsion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over







class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        beam = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/beam1.png')
        #Scales beam1.png. Use (x, y) to control size length, width
        self.image = pygame.transform.scale(beam, (10, 30))
        #self.image = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/beam1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        #controls when laser stops
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            #Explopsion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)



            #Create aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
       ## self.image = pygame.image.load("C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/alien" + str(random.randint(1, 2)) + ".png")
        #img = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/character.png')
        #self.image = pygame.transform.scale(img, (47, 99))
        img = pygame.image.load("C:/Users/arman/PycharmProjects/VideoGamesImages/Images/alien" + str(random.randint(1, 5)) + ".png")
        self.image = pygame.transform.scale(img, (49, 49))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        beam = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/beam1.png')
        #Scales beam1.png. Use (x, y) to control size length, width
        self.image = pygame.transform.scale(beam, (10, 30))
        #self.image = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/beam1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        #controls when laser stops
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        # pygame.sprite.collide_mask - helps for better accuracy
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            #kills bulldt
            self.kill()
            #reduce spaceship health
            spaceship.health_remaining -= 1

            #Explopsion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"C:/Users/arman/PycharmProjects/VideoGamesImages/Images/exp{num}.png")
            #if the size
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        #Scales beam1.png. Use (x, y) to control size length, width
        self.image = self.images[self.index]
        #self.image = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/beam1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
#Create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    #Generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)
create_aliens()

#create player
spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 200, 3)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    #draw background
    draw_bg()

    if countdown == 0:
        # create random alien bullets
        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        #IMPORTANT - CONTROLS HOW MANY ALIEN BULLETS ARE SHOT
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 8 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        # check if all the aliens have been killed
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()

            # update sprite groups
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font40, WHITE, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
            if game_over == 1:
                draw_text('YOU WIN!', font40, WHITE, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))

    if countdown > 0:
        draw_text('GET READY!', font40, WHITE, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 50))
        draw_text(str(countdown), font40, WHITE, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    # update explosion group
    explosion_group.update()

    # draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()