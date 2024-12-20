#https://www.youtube.com/watch?v=s5bd9KMSSW4&t=627s - citation
#START OF PixalFighter.py
# see hit boxes
import pygame

from Fighter3 import Fighter
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")
#Load background image


#Clcok
clock= pygame.time.Clock()
FPS = 60


#Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variable
#Count down in first match
intro_count = 0 # make 0 or 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#Define FIghter variable
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
#dispLAY CHARACTER LOCATION
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]


#load background image
bg_image = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/forest.png').convert_alpha()
#bg_image= pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/csusb library.png.convert_alpha()
#platform = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/platform.png').convert_alpha()


#load spritesheets
warrior_sheet = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/wizard.png').convert_alpha()


#load victory image
victory_img = pygame.image.load('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/victory.png').convert_alpha()


#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/turok.ttf', 80)
score_font = pygame.font.Font('C:/Users/005991267/OneDrive - California State University San Bernardino/Pictures/PyGame/turok.ttf', 80)

#Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


#Function for drawing health bars
def draw_health_bar(health, x, y):
    #Amount of health lose per hit
    ratio = health / 100

    #Color of the health bar as it decreases to 0
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#create two instances of fighter
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)


# game loop
run = True
while run:
    clock.tick(FPS)
    #draw background
    draw_bg()

    #Show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)    #update countdown
    if intro_count <= 0:
        # Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    #fighter_2.move()

    fighter_1.update()
    fighter_2.update()


    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #CHECK FOR PLAYER DEFEAT
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 0 #make 0 or 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

    #screen.blit(platform, (-10, -400))
    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#Exit pygame
pygame.quit()
#END OF PixalFighter.py

