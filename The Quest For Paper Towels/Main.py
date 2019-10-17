import pygame, sys, threading, time, random, os
from pygame.locals import *
from pygame.compat import geterror

pygame.init()

print(os.getcwd())

wait = lambda secs: time.sleep(secs)
screen = pygame.display.set_mode((500,900))
pygame.display.set_caption("The Quest For Paper Towels")
pygame.mouse.set_visible(0)
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 255, 0))
pygame.display.flip()

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect(), name

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.image, self.rect, self.sprite_path = load_image(r"C:\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\PH-enemy-name-left-still.png", -1)
        self.direction = "left"
        self.rect = self.rect.move((400,0))
        self.coordinates = [self.rect.x, self.rect.y]
        self.hit = 0
        self.move = 1
    def update(self, walking = False):
        #Update direction
        self.sprite_path = list(self.sprite_path)
        self.sprite_path = self.sprite_path.split("-")
        if "left" in self.sprite_path: #Is enemy facing left
            self.direction = "left"
        else:
            self.direction = "right"
        self.sprite_path = "".join(self.sprite_path)
        #Update status
        if self.hit:
            self.hit()
        if self.rect.colliderect(player.rect):
            self.attack()
        else:
            if not walking:
                self.walk()
        return
    def attack(self):
        pass
        self.original = self.image
    def hit(self):
        pass
        self.original = self.image
    def walk(self):
            if (player.coordinates[0] > self.coordinates[0]): #If player is right of enemy, move right
                if self.direction == "left":
                    self.image, self.rect, self.sprite_path = load_image(self.sprite_path_dict["right-still"], -1)

                self.rect = self.rect.move((self.move, 0))
                self.coordinates[0] += self.move
            else:
                self.rect = self.rect.move((-self.move, 0)) #Player is left of enemy; move left
                self.coordinates[0] += -self.move
            self.update(True)
            wait(0.01)
            if (player.coordinates[1] > self.coordinates[1]): #If player is above enemy, move up
                self.rect = self.rect.move((0, self.move))
                self.coordinates[1] += self.move
            else:
                self.rect = self.rect.move((0, -self.move)) #Player is below enemy; move down
                self.coordinates[1] += -self.move
            wait(0.01)
    sprite_path_dict = {
        "left-still": r"C:\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\PH-enemy-name-left-still.png",
        "left-moving": r"\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\PH-enemy-name-left-moving.png",
        "right-still": r"\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\PH-enemy-name-right-still.png",
        "right-moving": r"\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\New folder\Enemy-Sprites\PH-enemy-name-right-moving.png"
        }
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.health = 100
        self.image, self.rect = load_image(r"C:\Users\20LabB212\Documents\Game\Quest-For-Paper-Towels\blue-square.jpg", -1)
        self.area = screen.get_rect()
        self.coordinates = [self.rect.x, self.rect.y]
        self.walk_thread = threading.Thread(target=self.walk)
        self.hit = 0 #PROBLEM?
        self.walking = 0
        self.move = 5

    def player_input(self):
        while True:
            self.key = None
            pygame.event.pump()
            key = pygame.key.get_pressed()
            if key[K_w]:
                self.key = "w"
                self.walking = 1
                if not self.walk_thread.isAlive():
                    self.walk_thread.start()
            if key[K_a]:
                self.key = "a"
                self.walking = 1
                if not self.walk_thread.isAlive():
                    self.walk_thread.start()
            if key[K_s]:
                self.key = "s"
                self.walking = 1
                if not self.walk_thread.isAlive():
                    self.walk_thread.start()
            if key[K_d]:
                self.key = "d"
                self.walking = 1
                if not self.walk_thread.isAlive():
                    self.walk_thread.start()
            if key[K_f]:
                self.attack()
            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.walking = 0
                    self.walk_thread.join(1.0)

    def update(self):
        if self.hit:
            self.hit()
        if self.attack:
            self.attack()

    def walk(self):
        while self.walking:
            if (self.key == "w"):
                self.rect = self.rect.move((0, -self.move))
                self.coordinates[1] += -self.move
            if (self.key == "a") and not (self.rect.move((-self.move, 0)).colliderect(enemies.rect)): #Player cannot move through enemy (left)
                self.rect = self.rect.move((-self.move, 0))
                self.coordinates[0] += -self.move
            if (self.key == "s"):
                self.rect = self.rect.move((0, self.move))
                self.coordinates[1] += self.move
            if (self.key == "d") and not (self.rect.move((self.move, 0)).colliderect(enemies.rect)): #Player cannot move through enemy (right)
                self.rect = self.rect.move((self.move, 0))
                self.coordinates[0] += self.move
            print(self.coordinates) #PLAYER ICON DISAPPEARS WITHOUT THIS
            
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
                if player.walk_thread.isAlive():
                    player.walk_thread.join(0.1)
                if player_input.isAlive():
                    player_input.join(0.1)
                pygame.quit()
                sys.exit()
        all_sprites.update()
        screen.blit(background, (0,0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

player = Player()
enemies = Enemies()

player.key = None
player_input = threading.Thread(target=player.player_input)
player_input.start()

main()
