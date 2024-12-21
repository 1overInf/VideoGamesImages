#Infinite Jumps
#https://www.youtube.com/watch?v=W_JRd3ntyBg
#
#
import pygame
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1350
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 50
game_over = 0

#C:\Users\005991267\OneDrive - California State University San Bernardino\Pictures\PyGame
#example_image
sky = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/sky.png')
skyy = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/skyy.jpg')
skyyy = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/skyyy.png')

character = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/character.png')

chest = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/chest.png')

restart_img = pygame.image.load(('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/start button.png'))
#w = sky.get_width()
#h = sky.get_height()
#ww = chest.get_width()
#hh = chest.get_height()
#sky2 = pygame.transform.scale(sky, (w*0.5, h*0.5))
#chest2 = pygame.transform.scale(chest, (ww*.5, hh*.5))

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
        if game_over == 0:
            #get keypressed
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5

            #Add Gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #Check Collision
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

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                #print(game_over)



            #Update player coordinates
            self.rect.x += dx
            self.rect.y += dy


    ########Code checks to see if player has fallen off of map below. Can delete
            #if self.rect.bottom > screen_height:
             #   self.rect.bottom = screen_height
             #   dy = 0
        elif game_over == -1:
            self.image = self.dead_img
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
        dead_img = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/ghost.png')
        self.dead_img = pygame.transform.scale(dead_img, (47, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y = 0
        self.jumped = False

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
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x =  col_count * tile_size
                    img_rect.y =  row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x =  col_count * tile_size
                    img_rect.y =  row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size*1.006)
                    blob_group.add(blob)

                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    #lava = Lava(col_count * tile_size, row_count * tile_size * (tile_size // 2))

                    lava_group.add(lava)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        slime = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/slime.png')
        self.image = pygame.transform.scale(slime, (47, 47))


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        lava = pygame.image.load('C:/Users/arman/PycharmProjects/VideoGamesImages/Images/chest.png')
        self.image = pygame.transform.scale(lava, (47, 47))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
#Starting Position on Player
player = Player(100, screen_height - 600)

#player = Player(100, screen_height - 500)
#
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)

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


    blob_group.draw(screen)
    lava_group.draw(screen)
    game_over = player.update(game_over)

    #if PLAYER HAS DIED
    if game_over == -1:
        if restart_button.draw():
            player.reset(100, screen_height - 500)
            #spawns player, not ghost
            game_over = 0

            #Could delete bottom code???
            game_over = player.update(game_over)


    draw_grid()

    #print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()