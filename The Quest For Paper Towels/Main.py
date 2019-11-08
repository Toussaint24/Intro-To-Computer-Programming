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
    def __init__(self, images):
        super().__init__()
        self.index = 0
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]
        self.velocity = pygame.math.Vector2(0, 0)
        self.image = images[self.index]
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
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if self.velocity.x or self.velocity.y != 0:
                self.index = (self.index + 1) % len(self.images) # Alternate between sprites in list but prevents calling index out of range
                if self == player and self.index == 0:
                    self.index = (self.index + 1) % len(self.images) # Skip player attack animation while walking
                self.image = self.images[self.index]
            else:
                if self != player: 
                    self.image = self.images[0] # Keep still image if sprite is still
                else:
                    self.image = self.images[1] # Playe still image is second on the sheet

    def update(self, dt):
        self.update_time_dependent(dt)
        
class Player(AnimatedSprite):
    def __init__(self, health, strength, images):
        super().__init__(images)
        self.health = health
        self.strength = strength
        self.maxhealth = self.health
        self.attacking = 0
        self.attacked = 0

    def __repr__(self):
        return "Player"    

    def update(self, dt):
        super().update(dt)
        if self.health <= 0:
            self.die()

        elif self.attacked:
            if not self.hit_thread.isAlive():
                self.hit_thread = threading.Thread(target=self.hit, name="{} Hit Thread".format(self))
                self.hit_thread.start()

        elif self.attacking:
            self.attack()

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
        self.image = self.images[0]
        for enemy in Enemies.alive_group:
            if self.rect.colliderect(enemy.rect):
                enemy.attacked = 1
        self.attacking = 0

    def hit(self):
        for enemy in Enemies.alive_group:
            if self.rect.colliderect(enemy.rect):
                attacker = enemy
        if self.rect.x > enemy.rect.x:
            self.rect = self.rect.move((50, 0))
        elif enemy.rect.x > self.rect.x:
            self.rect = self.rect.move((-50, 0))
        self.health -= 1
        self.attacked = 0

    def die(self):
        sys.exit()

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
        self.hit_count = 0

    def __repr__(self):
            return self.name

    def spawn(self, enemy, location):
            self.rect = self.rect.move(location)
            self.alive_group.add(self)
            self.alive_enemies += 1

    def update(self, dt):
        if self.health <= 0:
            self.die()
        if self.attacked:
            if not self.hit_thread.isAlive():
                self.hit_thread = threading.Thread(target=self.hit, name="{} Hit Thread".format(self))
                self.hit_thread.start()
        elif self.rect.collidepoint(player.rect.center):
            if not player.attacking:
                if not self.attack_thread.isAlive():
                    self.attacking = 1
                    self.attack_thread = threading.Thread(target=self.attack, name="{} Attack Thread".format(self))
                    self.attack_thread.start()
        elif not self.attacked or not self.attacking:
                self.walk()
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
        player.attacked = 1
        self.attacking = 0
    
    def hit(self):
        self.hit_count += 1
        if player.rect.x > self.rect.x:
            self.rect = self.rect.move((-50, 0))
        elif self.rect.x > player.rect.x:
            self.rect = self.rect.move((50, 0))
        self.health -= 1
        wait(0.3)
        self.attacked = 0
        wait(0.5) # Invulnerability time after hit
    
    def die(self):
        self.alive_enemies -= 1
        self.sprite.remove(self.alive_group)
        self = self.copy

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

    def main(self):
        self.drawHealthMeter()
        stage_1.start()
        all_alive_group = pygame.sprite.RenderUpdates(Enemies.alive_group, player)
        running = True
        while running:
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

            all_alive_group.update(dt)
            screen.fill(BKGDCLR)
            all_alive_group.draw(screen)

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

player_ss = Spritesheets(os.path.join(player_sprite_path, "playersheet.png")).get_images(((0, 0, 32, 65), (35, 0, 38, 65), (70, 0, 38, 65), (105, 0, 38, 65)))
disgracer_ss = Spritesheets(os.path.join(enemy_sprite_path, "enemy-one-spritesheet.png")).get_images(((190, 5, 90, 140), (275, 5, 90, 140)))
pilgrim_ss = Spritesheets(os.path.join(enemy_sprite_path, "spritesheet (1).png")).get_images(((80, 0, 15, 65), (115, 0, 15, 65)))

player = Player(10, 2, player_ss)

disgracers = [None, None, None, None, None, None, None, None, None, None]
pilgrims = [None, None, None, None, None, None, None, None, None, None]

for slot in range(len(disgracers)):
    disgracers[slot] = Enemies("The Disgracer", str(slot+1), 4, 2, disgracer_ss)
    pilgrims[slot] = Enemies("The Pilgrim", str(slot+1), 8, 1, pilgrim_ss)
    

player_group = pygame.sprite.RenderUpdates(player)
enemy_sprites = pygame.sprite.Group(disgracers[0], pilgrims[0])

stage_1 = Stages(None, ((pilgrims[0], pilgrims[1]), ((400, 0), (0, 400))))

Main().main()
