#START OF Fighter.py
import pygame
class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle 1:run 2:jump 3:attack1 4: attack2 5:hit 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        #Jump trigger
        self.jump = False
        #Attack trigger
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True


    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            #Extract images from spritesheet
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        self.attack_type = 0
        #get keypressed
        key = pygame.key.get_pressed()
        #Can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #check playher 1 controls
            if self.player == 1:
            #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #Jump with w and
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attack

                if key[pygame.K_r] or key[pygame.K_t]:
                   #ATTACK appearing? surface is green attack block and target is enemy
                    self.attack(surface, target)
                    #determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2



            #check playher 2 controls
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #Jump with w and
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attack

                if key[pygame.K_m] or key[pygame.K_n]:
                   #ATTACK appearing? surface is green attack block and target is enemy
                    self.attack(surface, target)
                    #determine which attack type was used
                    if key[pygame.K_m]:
                        self.attack_type = 1
                    if key[pygame.K_n]:
                        self.attack_type = 2


        #Apply Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

######Boundrary for player on screen
        #left side
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        #Right side
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            #HELPS WITH JUMPS
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #Ensure player face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True


        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy


        #handle animation updates
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #6:death
        #CHeck what action the player is performing
        elif self.hit == True:
            self.update_action(5) #5:Hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)
        #controls speed of animation
        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        #Check if enough time has passed since  the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #if player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            # '- (2 * self.width * self.flip) ' flips character when passing over enemy
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            #If attack hits/ lands
            if attacking_rect.colliderect(target.rect):
            # print("Hit")
                target.health -= 10
                target.hit = True

            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        #check if the new action is different to the prevoius one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def draw(self, surface):
        #Flips chsaracter
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        #Flips chsaracter
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
#END OF Fighter.py