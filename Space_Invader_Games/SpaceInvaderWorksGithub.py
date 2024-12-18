from os import path
import pygame
import requests
from io import BytesIO
from PIL import Image

import random
import requests
import random

pygame.init()

# Define fps
clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invade')
#-------------------------------------------------------------------------

#----------------------------------------------------------------------------


# define fonts
font30 = pygame.font.SysFont('Bauhaus 93', 30)
font40 = pygame.font.SysFont('Bauhaus 93', 40)

# Define game variable
# Displays the aliens in a matrix (x, y) or (rows, cols)
rows = 5
cols = 5
# IMPORTANT - Control
alien_cooldown = 500  # bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()

countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0  # 0 is no game over, 1 means player has won, -1 means player has lost

# Define Color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
# Load space background image from GitHub
space_url = "https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/space.png"
response = requests.get(space_url)
space_data = response.content
pil_space = Image.open(BytesIO(space_data))
pil_space = pil_space.convert("RGBA")
pygame_space = pygame.image.fromstring(pil_space.tobytes(), pil_space.size, pil_space.mode)

# Convert to a surface that can be used with Pygame
bg = pygame_space.convert_alpha()

# Function for drawing background
def draw_bg():
    # SCALES BACKGROUND TO FIT SCREEN WIDTH AND HEIGHT
    scaled_bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # DISPLAYS SCALED BG
    screen.blit(scaled_bg, (0, 0))


# define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# def restart_game():
#     """Restart the game by resetting all variables"""
#     global spaceship, alien_group, bullet_group, alien_bullet_group, explosion_group, game_over, countdown, last_count, last_alien_shot
#
#     # Reset game variables
#     spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 200, 3)
#     spaceship_group.add(spaceship)
#
#     alien_group.empty()
#     bullet_group.empty()
#     alien_bullet_group.empty()
#     explosion_group.empty()
#
#     create_aliens()
#
#     countdown = 3
#     last_count = pygame.time.get_ticks()
#     game_over = 0
#     last_alien_shot = pygame.time.get_ticks()

# Load spaceship image from GitHub
spaceship_url = "https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/spaceship.png"
response = requests.get(spaceship_url)
spaceship_data = response.content
pil_spaceship = Image.open(BytesIO(spaceship_data))
pil_spaceship = pil_spaceship.convert("RGBA")
pygame_spaceship = pygame.image.fromstring(pil_spaceship.tobytes(), pil_spaceship.size, pil_spaceship.mode)

# In the Spaceship class, use pygame_spaceship as the image
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        # Use the dynamically loaded spaceship image
        self.image = pygame.transform.scale(pygame_spaceship, (60, 60))
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






# Load beam image from GitHub
beam_url = "https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/beam1.png"
response = requests.get(beam_url)
beam_data = response.content
pil_beam = Image.open(BytesIO(beam_data))
pil_beam = pil_beam.convert("RGBA")
pygame_beam = pygame.image.fromstring(pil_beam.tobytes(), pil_beam.size, pil_beam.mode)

# Now you can use `pygame_beam` as the image for the beam in your game

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the beam image from GitHub URL
        beam_url = "https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/beam1.png"
        response = requests.get(beam_url)
        beam_data = response.content

        pil_beam = Image.open(BytesIO(beam_data))  # Open image with Pillow
        pil_beam = pil_beam.convert("RGBA")  # Convert to RGBA format for compatibility with Pygame

        # Convert Pillow image to Pygame surface
        pygame_beam = pygame.image.fromstring(pil_beam.tobytes(), pil_beam.size, pil_beam.mode)

        # Scale the image to the desired size
        self.image = pygame.transform.scale(pygame_beam, (10, 30))  # Resize to 10x30
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]  # Set the initial position of the bullet

    def update(self):
        # Move the bullet upwards
        self.rect.y -= 5

        # Remove bullet when it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

        # Check collision with aliens
        collided_aliens = pygame.sprite.spritecollide(self, alien_group, True)

        if collided_aliens:
            self.kill()  # Kill the bullet upon collision

            # Create explosion at bullet's position if aliens are hit
            for alien in collided_aliens:
                # Create an explosion for each alien hit
                explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosion)

            #Create aliens class
import random
import requests
from io import BytesIO
from PIL import Image
import pygame

# Function to load alien image from GitHub
def load_alien_image(alien_number):
    alien_url = f"https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/alien{alien_number}.png"
    response = requests.get(alien_url)
    alien_data = response.content
    pil_alien = Image.open(BytesIO(alien_data))
    pil_alien = pil_alien.convert("RGBA")
    pygame_alien = pygame.image.fromstring(pil_alien.tobytes(), pil_alien.size, pil_alien.mode)
    return pygame_alien

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        alien_number = random.randint(1, 5)
        # Load alien image from URL
        img = load_alien_image(alien_number)
        self.image = pygame.transform.scale(img, (49, 49))  # Scale the image to desired size
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

import requests
from io import BytesIO
from PIL import Image
import pygame

# Function to load beam image from URL
def load_beam_image():
    beam_url = "https://raw.githubusercontent.com/1overInf/VideoGamesImages/main/beam1.png"
    response = requests.get(beam_url)
    beam_data = response.content
    pil_beam = Image.open(BytesIO(beam_data))
    pil_beam = pil_beam.convert("RGBA")
    pygame_beam = pygame.image.fromstring(pil_beam.tobytes(), pil_beam.size, pil_beam.mode)
    return pygame_beam

class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load beam image from URL
        beam = load_beam_image()
        # Scales the beam image. Use (x, y) to control size length, width
        self.image = pygame.transform.scale(beam, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        # Controls when laser stops
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        # Collision with spaceship (assuming spaceship_group is defined)
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # Reduce spaceship health (assuming spaceship object has a 'health_remaining' attribute)
            spaceship.health_remaining -= 1

            # Explosion effect (assuming Explosion is a defined class)
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# Function to load explosion image from URL
class Explosion(pygame.sprite.Sprite):
    # Preload the images only once (possibly at the beginning of the game)
    explosion_images = []
    for num in range(1, 6):
        img = pygame.image.load(f"C:/Users/arman/PycharmProjects/VideoGamesImages/exp{num}.png")
        explosion_images.append(img)

    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for img in Explosion.explosion_images:  # Use preloaded images
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            elif size == 2:
                img = pygame.transform.scale(img, (40, 40))
            elif size == 3:
                img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 5  # Adjust for animation speed
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

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
