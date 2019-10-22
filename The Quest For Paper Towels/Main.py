import pygame, sys, threading, time, random, os
from pygame.locals import *
from pygame.compat import geterror

pygame.init()

print(os.getcwd())

wait = lambda secs: time.sleep(secs)
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("The Quest For Paper Towels")
pygame.mouse.set_visible(0)
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 255, 0))
pygame.display.flip()

class Spritesheets: #HERE
    def __init__(self, filepath):
        self.sheet = pygame.image.load(filepath).convert()
    def get_image(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        return image
    def get_images(self, rects):
        return [self.get_image(rect) for rect in rects]

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.sprites = [] # Declare sprites list
        self.sprites = enemy_one_ss.get_images((0, 10, 90, 140), (90, 10, 90, 140), (180, 10, 90, 140), (270, 10, 90, 140)) #Get sprite images
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.direction = "left"
        self.rect = self.rect.move((400,0))
        self.coordinates = [self.rect.x, self.rect.y]
        self.hit = 0
        self.speed = [0, 0]
    def update(self):
        #Update direction
        self.direction = self.sprite_string_dict[self.image]
        #Update status
        if self.hit:
            self.hit()
        if self.rect.colliderect(player.rect):
            self.attack()
        else:
            self.walk()
    def attack(self):
        pass
        self.original = self.image
    def hit(self):
        pass
        self.original = self.image
    def walk(self):
        if (player.coordinates[0] > self.coordinates[0]): #If player is right of enemy, move right
            self.walk_animation("right-still")
            self.speed[0] += 1
            self.walk_animation("right-moving")
            self.speed[0] -= 1
            self.walk_animation("right-still")
            self.coordinates[0] += self.speed[0]
        else:
            self.rect = self.rect.move((-self.speed, 0)) #Player is left of enemy; move left
            self.coordinates[0] += -self.speed
        self.update(True)
        wait(0.01)
        if (player.coordinates[1] > self.coordinates[1]): #If player is above enemy, move up
            self.rect = self.rect.move((0, self.speed))
            self.coordinates[1] += self.speed
        else:
            self.rect = self.rect.move((0, -self.speed)) #Player is below enemy; move down
            self.coordinates[1] += -self.speed
        wait(0.01)
    def walk_animation(self, direction):
        self.image = self.string_sprite_dict[direction]
        self.direction = self.sprite_string_dict[self.image]
        self.rect = self.rect.move(self.speed)
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.health = 100
        self.image = pygame.image.load(r"C:\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\blue-square.jpg").convert()
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.coordinates = [self.rect.x, self.rect.y]
        self.hit = 0 #PROBLEM?
        self.moving = 0
        self.speed = [0, 0]

    def update(self):
        if self.hit:
            self.hit()
        if self.attack:
            self.attack()
        self.walk()

    def walk(self):
        self.rect = self.rect.move((self.speed[0], self.speed[1]))
        self.coordinates = [self.rect.x, self.rect.y]
            
    def hit(self):
        self.original = self.image
        self.rect = self.rect.move((10, 0))
        for i in range(255):
            self.image = pygame.Surface.fill((i, 0, 0), self.rect)
        for i in range(255, 0):
            self.image = pygame.Surface.fill((i, 0, 0), self.rect)
        wait(4)
        self.image = self.original
    def attack(self):
        self.original = self.image
    def get_healthbar(self):
        pass

def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.RenderPlain((player, enemies))
    on = True
    while on:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    player.speed[1] -= 5
                if event.key == K_a:
                    player.speed[0] -= 5
                if event.key == K_s:
                    player.speed[1] += 5
                if event.key == K_d:
                    player.speed[0] += 5
                print(player.speed)
            if event.type == KEYUP:
                if event.key == K_w:
                    player.speed[1] += 5
                if event.key == K_a:
                    player.speed[0] += 5
                if event.key == K_s:
                    player.speed[1] -= 5
                if event.key == K_d:
                    player.speed[0] -= 5
        all_sprites.update()
        screen.blit(background, (0,0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

player = Player()
enemies = Enemies()
enemy_one_ss = Spritesheets(r"C:\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\enemy-one-spritesheet.png")

sprite_string_dict = {
    enemies.sprites[0]: "left-still",
    enemies.sprites[1]: "left-moving",
    enemies.sprites[2]: "right-still",
    enemies.sprites[3]: "right-moving"
    }
string_sprite_dict = {
    "left-still": enemies.sprites[0],
    "left-moving": enemies.sprites[1],
    "right-still": enemies.sprites[2],
    "right-moving": enemies.sprties[3]
    }

main()
