#Multi level Game and Code stops once q is pressed
#https://www.youtube.com/watch?v=W_JRd3ntyBg
#
#
from os import path

import pygame
import pickle
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1350
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
#Define color
white = (255, 255, 255)
blue = (0, 0, 255)
#DEFINE Game Variables
tile_size = 50
game_over = 0
level = 0
max_levels = 4
score = 0

#C:/Users/arman/PycharmProjects/VideoGamesImages/Images/PyGame
#example_image

# sky = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/sky.png')
skyy = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/skyy.jpg')
skyyy = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/skyyy.png')

character = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/character.png')

# chest = pygame.image.load('C:C:/Users/arman/PycharmProjects/VideoGamesImages/Images/chest.png')
restart_img = pygame.image.load(('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/CHESS.png'))


#FUnction
def draw_text(text, font, text_col, x, y):
    imgg = font.render(text, True, text_col)
    screen.blit(imgg, (x, y))


#Function to reset level
def reset_level(level):
    player.reset(100, screen_height - 500)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()
    bee_group.empty()

    treasure_group.empty()

    #If statement checks to make sure level exist
    if path.exists(f'level{level}_data'):
        #load in level data and create world
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            #print('Mouse Over')
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                #print('CLICKED')
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        screen.blit(self.image, self.rect)
        return action

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
    def __init__(self, x, y):
        self.reset(x, y)
    def update(self, game_over):
        dx = 0
        dy = 0
        col_thresh = 20
        if game_over == 0:
            #get keypressed
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False :
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5
            if key[pygame.K_q]:
                pygame.quit()

            #Add Gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #Check Collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e.  jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #Check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            #Check for collision with enemies
            if pygame.sprite.spritecollide(self, bee_group, False):
                game_over = -1
            #Check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            # Check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
                #print(game_over)
            # Check for collision with treasure - exit
            if pygame.sprite.spritecollide(self, treasure_group, False):
                game_over = 1

            #Check for collision with platforms
            for platform in platform_group:
                #Collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #Check if above platform- aka having player land on platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction


            #Update player coordinates
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_img
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
            #PART 1. ENDLESSLY GHOST FLIES UP
            #self.rect.y -= 5
            #PART 2 Once certain height reached, ghost disaapears
            if self.rect.y > 200:
                self.rect.y -= 5
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        return game_over

    def reset(self, x, y):

        self.index = 0
        self.counter = 0
        img = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/character.png')
        self.image = pygame.transform.scale(img, (47, 99))
        dead_img = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/Ghost.png')
        self.dead_img = pygame.transform.scale(dead_img, (47, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y = 0
        self.jumped = False
        self.in_air = True
class World():

    def __init__(self, data):
        self.tile_list = []
        #load Images
        dirt_img = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/dirt.png')
        grass_img = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/grass.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                #dirt block
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x =  col_count * tile_size
                    img_rect.y =  row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #Grass block
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x =  col_count * tile_size
                    img_rect.y =  row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #ENEMY-Slime
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size*1.006)
                    blob_group.add(blob)

                #Surface-Platform
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                #Surface-Platform
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                #ENEMY - LAVA
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    #lava = Lava(col_count * tile_size, row_count * tile_size * (tile_size // 2))

                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size, row_count * tile_size*1.006)
                    coin_group.add(coin)
                #LEVEL COMPLETE MARKER - Exit
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size)

                    exit_group.add(exit)
                #GAME COMPLETE MARKER - Exit
                if tile == 9:
                    treasure = Treasure(col_count * tile_size, row_count * tile_size)

                    treasure_group.add(treasure)
                #ENEMY - BEE
                if tile == 10:
                    bee = Bee(col_count * tile_size, row_count * tile_size*1.006)
                    bee_group.add(bee)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

#World Class - Tile 3 - Slime
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)


        slime = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/slime.png')
        self.image = pygame.transform.scale(slime, (25, 25))


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
#Movement - Slime
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

#World Class - Tile 10 - BEE
class Bee(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bee = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/bee.png')
        self.image = pygame.transform.scale(bee, (44, 44))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
#Movement - BEE
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1



#World Class - Tile 6
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        lava = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/lava.png')
        self.image = pygame.transform.scale(lava, (47, 47))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



#World Class - Tile 8 - Exit

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        exit = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/portal.png')
        self.image = pygame.transform.scale(exit, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# WORLD CLASS - TILE 9 TREASURE CHEST
class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        treasure = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/chest.png')
        self.image = pygame.transform.scale(treasure, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#World Class - Tile 7
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        coin = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/coin.png')
        self.image = pygame.transform.scale(coin, (47, 47))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        platform = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/platform.png')
        self.image = pygame.transform.scale(platform, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y

        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

#WORLD LEVEL DESIGN


#Starting Position on Player
player = Player(100, screen_height - 600)

#player = Player(100, screen_height - 500)
#

exit_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
treasure_group = pygame.sprite.Group()
bee_group = pygame.sprite.Group()

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

#Create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)

#If statement checks to make sure level exist
if path.exists(f'level{level}_data'):

    #load in level data and create world
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

run = True
while run:
    clock.tick(fps)
    screen.blit(skyy, (-10, -400))
    #screen.blit(sky2, 300, 50)
    #screen.blit(chest, (50, 250))
    #screen.blit(chest2, (300, 250))
    world.draw()

    if game_over == 0:
        blob_group.update()
        bee_group.update()

        platform_group.update()
        #update score
        #check if a coin has been collected
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
        draw_text('X '+ str(score), font_score, white, tile_size +10, screen_height -1030)

    exit_group.draw(screen)
    blob_group.draw(screen)
    platform_group.draw(screen)
    treasure_group.draw(screen)
    bee_group.draw(screen)

    lava_group.draw(screen)
    coin_group.draw(screen)
    game_over = player.update(game_over)

    #if PLAYER HAS DIED
    if game_over == -1:
        if restart_button.draw():
            world_data = []
            world = reset_level(level)
            #player.reset(100, screen_height - 500)
            #spawns player, not ghost
            game_over = 0
            score = 0

    #If player has completed the level
    if game_over == 1:
        #reset game and go to next level
        level += 1
        if level <= max_levels:
            #Reset level
            world_data = []
            world = reset_level(level)
            game_over = 0
        else:
            #Prints you when once max level reached
            draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height -900)
            #restart game
            if restart_button.draw():
                level = 0
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

    #draw_grid()

    #print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Stop with Q key pressed
    #key = pygame.keyy.get_pressed()
key = pygame.key.get_pressed()