import pygame
import random
import os

WIDTH = 1920
HEIGHT = 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()
sky_img = pygame.image.load(os.path.join(img_folder, '123.png')).convert()
snow_img = pygame.image.load(os.path.join(img_folder, 'snow.png')).convert()
sword_right_img = pygame.image.load(os.path.join(img_folder, 'sword1.png')).convert()
sword_left_img = pygame.image.load(os.path.join(img_folder, 'sword2.png')).convert()
enemy_img = pygame.image.load(os.path.join(img_folder, 'flyFly1.png')).convert()
agr_img = pygame.image.load(os.path.join(img_folder, 'agr.png')).convert()
hp_img = pygame.image.load(os.path.join(img_folder, 'hp.png')).convert()

x, y = WIDTH / 2, HEIGHT - 230
x1, y1 = WIDTH / 2, HEIGHT - 600
x2, y2 = 210, 130


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (WIDTH / 2, HEIGHT - 260)

    def update(self):
        global x, y, sword_right, sword_left
        sword_right = Sword_right()
        sword_left = Sword_left()
        x, y = self.rect.x, self.rect.y
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        mousestate = pygame.mouse.get_pressed()
        if keystate[pygame.K_x]:
            all_sprites.add(sword_right)
            all_sprites.add(sword_left)
        if mousestate[0]:
            pass
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Snow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snow_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (WIDTH - 300, HEIGHT + 200)


class Sword_right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sword_right_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x + 100, y + 20)


class Sword_left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sword_left_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x - 37, y + 25)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.flag = False
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (WIDTH / 2, HEIGHT - 600)

    def update(self):
        global x1, y1, agr
        count = 0
        x1, y1 = self.rect.x, self.rect.y
        self.speedy, self.speedx = 0, 0
        self.speedy, self.speedx = random.randint(-1, 2), random.randint(-1, 2)
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        agr = Provocation()
        if y - y1 < 100:
            all_sprites.add(agr)

    def coords(self):
        return x1, y1


class Provocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = agr_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        coords = []
        for i in enemy.coords():
            coords.append(i)
        self.rect.center = (coords[0] + 40, coords[1] - 30)


class HPbar(pygame.sprite.Sprite):
    global x2, y2
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hp_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x2, y2)


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
snow = Snow()
all_sprites.add(snow)
enemy = Enemy()
all_sprites.add(enemy)
for i in range(1, 11):
    hp = HPbar()
    all_sprites.add(hp)
    x2 += 30

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    screen.blit(sky_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    sword_right.kill()
    sword_left.kill()
    agr.kill()

pygame.quit()
