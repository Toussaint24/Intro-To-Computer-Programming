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
        self.hit_thread = threading.Thread(target=self.hit)
        self.attack_thread = threading.Thread(target=self.attack)

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.
        """
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.walk_images = self.walk_images_right
        elif self.velocity.x < 0:
            self.walk_images = self.walk_images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if self.velocity.x or self.velocity.y != 0:
                self.index = (self.index + 1) % len(self.walk_images) # Alternate between sprites in list but prevents calling index out of range
                self.image = self.walk_images[self.index]
            else:
                self.image = self.images[0] # Keep still image if sprite is still

    def update(self, dt):
        self.update_time_dependent(dt)
        
class Player(AnimatedSprite):
    def __init__(self, health, strength, walk_images, attack_image):
        super().__init__(walk_images)
        self.health = health
        self.strength = strength
        self.maxhealth = self.health
        self.attack_image = attack_image
        self.arm = Arm(self.attack_image)
        self.lives = 3
        self.attacking = 0
        self.attacked = 0

    def __repr__(self):
        return "Player"    

    def update(self, dt):
        super().update(dt)
        if self.health <= 0:
            self.die()
        if 

        if self.velocity.x == -4 and self.rect.x < player.velocity.x: # W
            self.velocity.x += 4
        elif self.velocity.x == 4 and self.rect.x > screen.get_size()[0] - self.rect.width - self.velocity.x: # S
            self.velocity.x -= 4
        if self.velocity.y == -4 and self.rect.y < player.velocity.y: # A
            self.velocity.y += 4
        elif self.velocity.y == 4 and self.rect.y > screen.get_size()[1] - self.rect.height - self.velocity.y: # D
            self.velocity.y -= 4

        self.rect = self.rect.move((self.velocity.x, self.velocity.y))

    def attack(self):
        self.image = self.attack_image
        for enemy in Enemies.alive_group:
            if self.arm.get_rect().colliderect(enemy.rect): #HERE
                enemy.attacked = 1
        self.attacking = 0

    def hit(self):
        pass

    def die(self):
        if self.lives == 0:
            sys.exit()
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
    def __init__(self, name, number, health, strength, sprites):
        super().__init__(sprites)
        self.copy = self
        self.name = name + "_" + number
        self.health = health
        self.strength = strength
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
        super().update(dt)
        self.velocity.x, self.velocity.y = 0, 0

    def walk(self):
        if player.rect.x > self.rect.x: #Player is right of enemy
            self.velocity.x += 1.5
        elif self.rect.x > player.rect.x:
            self.velocity.x -= 1.5
        if player.rect.y > self.rect.y: #Player is below enemy
            self.velocity.y += 1.5
        elif self.rect.y > player.rect.y:
            self.velocity.y -= 1.5
        self.rect = self.rect.move((self.velocity.x, self.velocity.y))
        
    def attack(self):
        pass
    
    def hit(self):
        pass
    
    def die(self):
        self.alive_enemies -= 1
        self.remove(self.alive_group)

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
        self.hit_count += 1
        self.health -= 1
        wait(0.1)
        self.attacked = 0
    
    def die(self):
        self.remove(Enemies.alive_group)

class Stages:
    def __init__(self, background, enemy_information):
        self.background = background
        self.enemy_list = enemy_information[0]
        self.location_list = enemy_information[1]
        self.enemy_count = len(enemy_information[0])
        self.enemy_types = set(enemy_information[0])

    def start(self):
        """Initializes the stage by drawing the background and spawning the enemies"""
        if self.background != None:
            screen.blit(self.background, (0, 0))
        for enemy in range(len(self.enemy_list)):
            self.enemy_list[enemy].spawn(self.enemy_list[enemy], self.location_list[enemy])

class Main: #basically everything to make it work properly
    def __init__(self):
        pass

    def main(self):
        self.drawHealthMeter()
        stage_1.start()
        running = True
        while running:
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

player_walk_sprites = Spritesheets(os.path.join(player_sprite_path, "playersheet.png")).get_images(((0, 0, 32, 65), (70, 0, 38, 65), (105, 0, 38, 65)))
player_attack_sprite = Spritesheets(os.path.join(player_sprite_path, "playersheet.png")).get_image((35, 0, 38, 65))
disgracer_ss = Spritesheets(os.path.join(enemy_sprite_path, "enemy-one-spritesheet.png")).get_images(((190, 5, 90, 140), (275, 5, 90, 140)))
pilgrim_ss = Spritesheets(os.path.join(enemy_sprite_path, "spritesheet (1).png")).get_images(((80, 0, 15, 65), (115, 0, 15, 65)))
boss_ss = Spritesheets(os.path.join(enemy_sprite_path, "BossSheet.png")).get_images(((90, 0, 90, 140), (180, 0, 90, 140), (270, 0, 90, 140)))

player = Player(10, 2, player_walk_sprites, player_attack_sprite)

disgracers = [None, None, None, None, None, None, None, None, None, None]
pilgrims = [None, None, None, None, None, None, None, None, None, None]
boss = Boss("Boss", 10, 2, boss_ss)

for slot in range(len(disgracers)):
    disgracers[slot] = Enemies("The Disgracer", str(slot+1), 4, 2, disgracer_ss)
    pilgrims[slot] = Enemies("The Pilgrim", str(slot+1), 8, 1, pilgrim_ss)
    

player_group = pygame.sprite.RenderUpdates(player)
enemy_sprites = pygame.sprite.Group(disgracers[0], pilgrims[0])
stage_1 = Stages(None, ((pilgrims[0], pilgrims[1]), ((400, 0), (0, 400))))

Main = Main()
Main.main()
