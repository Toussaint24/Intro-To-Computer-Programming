import pygame, sys, threading, time, random, os
from pygame.locals import *
from pygame.compat import geterror

pygame.init()

ORANGE = (194, 98, 0)
BKGDCLR = (0, 128, 128)
FPS = 60

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("The Quest For Paper Towels Experiment")
background = pygame.Surface(screen.get_size()).convert()

LEFT_BORDER = 0
RIGHT_BORDER = screen.get_size()[0]
TOP_BORDER = 0
BOTTOM_BORDER = screen.get_size()[1]
BORDERS = (0, 0, screen.get_size()[0], screen.get_size()[1])

background.fill(BKGDCLR)
pygame.display.flip()

clock = pygame.time.Clock()
wait = lambda secs: time.sleep(secs)

current_path = os.path.dirname(__file__)
resource_path = os.path.join(current_path, "Images")
player_sprite_path = os.path.join(resource_path, "Player-Spritesheet")
enemy_sprite_path = os.path.join(resource_path, "Enemy-Sprites")

class Spritesheets: #HERE
    def __init__(self, filepath):
        self.sheet = pygame.image.load(filepath).convert()
        
    def get_image(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.set_colorkey(ORANGE)
        image.blit(self.sheet, (0, 0), rect)
        return image
        
    def get_images(self, rects):
        images = []
        for rect in rects:
            images.append(self.get_image(rect))
        return images

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, walk_images):
        super().__init__()
        self.index = 0
        self.walk_images = walk_images
        self.walk_images_right = walk_images
        self.walk_images_left = [pygame.transform.flip(image, True, False) for image in walk_images]
        self.velocity = pygame.math.Vector2(0, 0)
        self.image = walk_images[self.index]
        self.rect = self.image.get_rect()
        self.animation_time = 0.1
        self.current_time = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.
        """
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.walk_images = self.walk_images_right
            self.direction = "Right"
        elif self.velocity.x < 0:
            self.walk_images = self.walk_images_left
            self.direction = "Left"

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if self.velocity.x or self.velocity.y != 0:
                self.index = (self.index + 1) % len(self.walk_images) # Alternate between sprites in list but prevents calling index out of range
                self.image = self.walk_images[self.index]
            else:
                self.image = self.walk_images[0] # Keep still image if sprite is still

    def update(self, dt):
        self.update_time_dependent(dt)
        
class Player(AnimatedSprite):
    def __init__(self, health, strength, walk_images, attack_image):
        super().__init__(walk_images)
        self.health = health
        self.strength = strength
        self.maxhealth = self.health
        self.attack_image = attack_image
        self.attack_image_left = pygame.transform.flip(attack_image, True, False)
        self.arm = Arm(self.attack_image)
        self.rect = self.rect.move((0, BOTTOM_BORDER/2))
        self.lives = 3
        self.attacking = 0
        self.attacked = 0

    def __repr__(self):
        return "Player"    

    def update(self, dt):
        super().update(dt)
        if self.health <= 0:
            self.die()
        if self.attacked:
            self.hit()
        elif self.attacking:
            self.attack()

        if self.velocity.x == -4 and self.rect.x < player.velocity.x: # W
            self.velocity.x += 4
        elif self.velocity.x == 4 and self.rect.x > RIGHT_BORDER - self.rect.width - self.velocity.x: # S
            self.velocity.x -= 4
        if self.velocity.y == -4 and self.rect.y < player.velocity.y: # A
            self.velocity.y += 4
        elif self.velocity.y == 4 and self.rect.y > BOTTOM_BORDER - self.rect.height - self.velocity.y: # D
            self.velocity.y -= 4

        self.rect = self.rect.move((self.velocity.x, self.velocity.y))

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > RIGHT_BORDER - self.rect.width:
            self.rect.x = RIGHT_BORDER
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > BOTTOM_BORDER - self.rect.height:
            self.rect.y = BOTTOM_BORDER

    def attack(self):
        if self.direction == "Right":
            self.image = self.attack_image
        elif self.direction == "Left":
            self.image = self.attack_image_left
        for enemy in Enemies.alive_group:
            if self.arm.get_rect().colliderect(enemy.rect): #HERE
                enemy.attacked = 1
        self.attacking = 0

    def hit(self):
        attackers = []

        for enemy in Enemies.alive_group:
            if enemy.rect.collidepoint(self.rect.center):
                attackers.append(enemy)

        if len(attackers) != 0:
            if self.rect.x > attackers[0].rect.x:
                self.rect = self.rect.move(-50, 0)
            else:
                self.rect = self.rect.move(50, 0)
            self.health -= 1

        self.attacked = 0

    def die(self):
        if self.lives == 0:
            Main.running = False
        else:
            self.lives -= 1

class Arm:
    def __init__(self, image):
        self.image = image.subsurface((18, 30, 14, 13))
        self.rect = self.image.get_rect()

    def get_rect(self):
        self.rect.x = player.rect.x + self.image.get_offset()[0]
        self.rect.y = player.rect.y + self.image.get_offset()[1]
        return self.rect

class Enemies(AnimatedSprite):
    enemy_list = {}
    alive_group = pygame.sprite.Group()
    def __init__(self, name, number, health, strength, speed, kb_distance, sprites):
        super().__init__(sprites)
        self.copy = self
        self.name = name + "_" + number
        self.health = health
        self.strength = strength
        self.speed = speed
        self.kb_distance = kb_distance
        self.enemy_list[self.name] = self
        self.alive_enemies = 0
        self.attacked = 0

    def __repr__(self):
            return self.name

    def spawn(self, enemy, location):
            self.rect = self.rect.move(location)
            self.alive_group.add(self)
            self.alive_enemies += 1

    def update(self, dt):
        if self.health <= 0:
            self.die()

        for enemy in self.alive_group:
            if self.rect.collidepoint(enemy.rect.center):
                if enemy != self:
                    self.rect = self.rect.move((50, 0))

        self.walk()
        super().update(dt)
        self.velocity.x, self.velocity.y = 0, 0

        if self.attacked:
            self.hit()
        if self.rect.collidepoint(player.rect.center): #if self.thing += dt > 0.5?
            self.attack()

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > RIGHT_BORDER - self.rect.width:
            self.rect.x = RIGHT_BORDER
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > BOTTOM_BORDER - self.rect.height:
            self.rect.y = BOTTOM_BORDER

    def walk(self):
        if player.rect.center[0] > self.rect.center[0]:
            self.velocity.x += self.speed
        elif self.rect.center[0] > player.rect.center[0]:
            self.velocity.x -= self.speed
        if player.rect.center[1] > self.rect.center[1]:
            self.velocity.y += self.speed
        elif self.rect.center[1] > player.rect.center[1]:
            self.velocity.y -= self.speed
        self.rect = self.rect.move((self.velocity.x, self.velocity.y))
        
    def attack(self):
        player.attacked = 1
    
    def hit(self):
        if self.rect.x < player.rect.x:
            self.rect = self.rect.move(-self.kb_distance, 0)
        else:
            self.rect = self.rect.move(self.kb_distance, 0)
        self.health -= 1
        self.attacked = 0

    
    def die(self):
        self.alive_enemies -= 1
        self.remove(self.alive_group)
        self = self.copy

class Boss(AnimatedSprite):
    boss_list = {}
    def __init__(self, name, health, strength, sprites):
        super().__init__(sprites)
        self.name = name
        self.health = health
        self.strength = strength
        self.boss_list[name] = self

    def __repr__(self):
        return self.name

    def spawn(self):
        pass

    def update(self, dt):
        pass 

    def walk(self):
        pass

    def attack(self):
        pass

    def hit(self):
        self.health -= 1
        self.attacked = 0
    
    def die(self):
        self.remove(Enemies.alive_group)

class Stages:
    stages_completed = [False, False, False]
    waves_completed = [False, False, False]

    def __init__(self, background, w1_enemy_information, w2_enemy_information, w3_enemy_information):
        self.background = background

        self.enemy_list_1 = w1_enemy_information[0]
        self.location_list_1 = w1_enemy_information[1]
        self.enemy_count_1 = len(w1_enemy_information[0])
        self.enemy_types_1 = set(w1_enemy_information[0])

        self.enemy_list_2 = w2_enemy_information[0]
        self.location_list_2 = w2_enemy_information[1]
        self.enemy_count_2 = len(w2_enemy_information[0])
        self.enemy_types_2 = set(w2_enemy_information[0])

        self.enemy_list_3 = w3_enemy_information[0]
        self.location_list_3 = w3_enemy_information[1]
        self.enemy_count_3 = len(w3_enemy_information[0])
        self.enemy_types_3 = set(w3_enemy_information[0])

    def start(self):
        """Initializes the stage by drawing the background and spawning the enemies"""

        if self.background != None:
            screen.blit(self.background, (0, 0))

        if self.waves_completed.count(True) == 0:
            for enemy in range(len(self.enemy_list_1)):
                self.enemy_list_1[enemy].spawn(self.enemy_list_1[enemy], self.location_list_1[enemy])

        elif self.waves_completed.count(True) == 1:
            for enemy in range(len(self.enemy_list_2)):
                self.enemy_list_2[enemy].spawn(self.enemy_list_2[enemy], self.location_list_2[enemy])

        elif self.waves_completed.count(True) == 2:
            for enemy in range(len(self.enemy_list_2)):
                self.enemy_list_2[enemy].spawn(self.enemy_list_2[enemy], self.location_list_2[enemy])

    def new_wave(self):
        if not all(self.waves_completed):
            self.waves_completed.remove(False)
            self.waves_completed.append(True)
        else:
            Stages.stages_completed.remove(False)
            Stages.stages_completed.append(True)
            if Stages.stages_completed.count(True) == 1:
                stage_2.start()
            elif Stages.stages_completed.count(True) == 2:
                stage_3.start()
            elif Stages.stages_completed.count(True) == 3:
                Main._quit()

class Main: #basically everything to make it work properly
    def main(self):
        self.drawHealthMeter()
        stage_1.start()
        self.running = True
        while self.running:
            self.all_alive_group = pygame.sprite.RenderUpdates(Enemies.alive_group, player)
            self.drawHealthMeter()
            dt = clock.tick(FPS) / 1000.0 #Time between frames
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        player.velocity.y -= 4
                    if event.key == K_a:
                        player.velocity.x -= 4
                    if event.key == K_s:
                        player.velocity.y += 4
                    if event.key == K_d:
                        player.velocity.x += 4
                    if event.key == K_f:
                        player.attacking = 1
                if event.type == KEYUP:
                    if event.key == K_w and player.velocity.y == -4:
                        player.velocity.y += 4
                    if event.key == K_a and player.velocity.x == -4:
                        player.velocity.x += 4
                    if event.key == K_s and player.velocity.y == 4:
                        player.velocity.y -= 4
                    if event.key == K_d and player.velocity.x == 4:
                        player.velocity.x -= 4

            if len(Enemies.alive_group) == 0:
                if Stages.stages_completed == 0:
                    stage_1.new_wave()
                elif Stages.stages_completed == 1:
                    stage_2.new_wave()
                elif Stages.stages_completed == 2:
                    stage_3.new_wave()

            self.all_alive_group.update(dt)
            screen.fill(BKGDCLR)
            self.all_alive_group.draw(screen)
            pygame.display.update()

        self._quit()

    def drawHealthMeter(self):
        for i in range(player.health): # draw red health bars
            pygame.draw.rect(screen, (255, 0, 0),   (15, 5 + (10 * player.maxhealth) - i * 10, 20, 10))
        for i in range(player.maxhealth): # draw the white outlines
            pygame.draw.rect(screen, (255, 255, 255), (15, 5 + (10 * player.maxhealth) - i * 10, 20, 10), 1)
        pygame.display.update()

    def _quit(self):
        pygame.quit()
        sys.exit()

player_walk_sprites = Spritesheets(os.path.join(player_sprite_path, "playersheet.png")).get_images(((35, 0, 38, 65), (70, 0, 38, 65), (105, 0, 38, 65)))
player_attack_sprite = Spritesheets(os.path.join(player_sprite_path, "playersheet.png")).get_image((0, 0, 32, 65))
disgracer_ss = Spritesheets(os.path.join(enemy_sprite_path, "enemy-one-spritesheet.png")).get_images(((190, 5, 90, 140), (275, 5, 90, 140)))
pilgrim_ss = Spritesheets(os.path.join(enemy_sprite_path, "spritesheet (1).png")).get_images(((80, 0, 15, 65), (115, 0, 15, 65)))
boss_ss = Spritesheets(os.path.join(enemy_sprite_path, "BossSheet.png")).get_images(((90, 0, 90, 140), (180, 0, 90, 140), (270, 0, 90, 140)))

player = Player(10, 2, player_walk_sprites, player_attack_sprite)

disgracers = [None, None, None, None, None, None, None, None, None, None]
pilgrims = [None, None, None, None, None, None, None, None, None, None]
boss = Boss("Boss", 10, 2, boss_ss)

for slot in range(len(disgracers)):
    disgracers[slot] = Enemies("The Disgracer", str(slot+1), 4, 2, 3, 50, disgracer_ss)
    pilgrims[slot] = Enemies("The Pilgrim", str(slot+1), 8, 1, 1.5, 25, pilgrim_ss)
    

player_group = pygame.sprite.RenderUpdates(player)
enemy_sprites = pygame.sprite.Group(disgracers[0], pilgrims[0])
stage_1 = Stages(None, 
                    ((disgracers[0], disgracers[1]), #Wave 1
                        (RIGHT_BORDER, BOTTOM_BORDER/2), (RIGHT_BORDER, BOTTOM_BORDER/2)),
                    ((disgracers[0], disgracers[1], disgracers[2], disgracers[3]), #Wave 2
                        (LEFT_BORDER, RIGHT_BORDER), (LEFT_BORDER, BOTTOM_BORDER), (RIGHT_BORDER/2, BOTTOM_BORDER/2), (RIGHT_BORDER/2, BOTTOM_BORDER/2)),
                    ((disgracers[0], disgracers[1], disgracers[2], disgracers[3], disgracers[4], disgracers[5]), #Wave 3
                        (player.rect.x+35, BOTTOM_BORDER/2), (0, player.rect.y-50), (0, player.rect.y+50), (0, 0), (RIGHT_BORDER, BOTTOM_BORDER), (RIGHT_BORDER/2, BOTTOM_BORDER/2)))

stage_2 = Stages(None,
                    ((disgracers[0], pilgrims[0]), #Wave 1
                        (0, 0), (0, 0)),
                    ((disgracers[0], pilgrims[0], pilgrims[1]), #Wave 2
                        (0, 0), (0, 0), (0, 0)),
                    ((pilgrims[0], pilgrims[1], pilgrims[2], pilgrims[3], pilgrims[4]), #Wave 3
                        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)))

stage_3 = Stages(None,
                    ((disgracers[0], disgracers[1], pilgrims[0], pilgrims[1]), #Wave 1
                        (500, 100), (375, 260), (100, 300), (375, 340)),
                    ((disgracers[0], disgracers[1], disgracers[2], disgracers[3], pilgrims[0], pilgrims[1], pilgrims[2]), #Wave 2
                        (515, 557), (350, 500), (472, 390), (305, 0), (240, 160), (225, 250), (150, 200)),
                    ((boss),
                        (90,550)))

Main = Main()
Main.main()
