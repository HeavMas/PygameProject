import pygame
import os

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640
FPS = 30
MAPS_DIR = "maps"
TILE_SIZE = 24


class Map:
    def __init__(self, filename, free_tiles):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (120, 120, 120), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


class Hero:
    def __init__(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 255), center, TILE_SIZE // 2)

class Weapon:

    def __init__(self):
        pass

    def render(self, screen, pos):
        if pygame.key.get_pressed()[pygame.K_x]:
            pygame.draw.circle(screen, (255, 0, 0), pos, 100, 10)


class Game:

    def __init__(self, map, hero, weapon):
        self.map = map
        self.hero = hero
        self.weapon = weapon

    def render(self, screen):
        self.map.render(screen)
        self.hero.render(screen)
        self.weapon.render(screen, (self.hero.get_position()[0] * (TILE_SIZE + 1),
                                    self.hero.get_position()[1] * (TILE_SIZE + 1)))

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_w]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            next_y += 1
        if self.map.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def AttackAnimation(self, screen):
        self.weapon.render(screen, self.hero.get_position())



def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    map = Map("Map.txt", [0, 1])
    hero = Hero((12, 22))
    weapon = Weapon()
    game = Game(map, hero, weapon)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
