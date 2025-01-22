import pygame
import math

from numpy.lib.function_base import angle
from pygame.transform import rotate

from map import Map

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
tile_width = tile_height = 45
tile_images = {
    'empty': pygame.transform.scale(pygame.image.load('data/pol.png'), (tile_width, tile_height)),
    'wall-gor': pygame.transform.scale(pygame.image.load('data/wall_gorizont.png'), (tile_width, tile_height)),
    'wall-vert': pygame.transform.scale(pygame.image.load('data/wall_vert_sverhu.png'), (tile_width, tile_height)),
    'wall-vert-pov-r': pygame.transform.scale(pygame.image.load('data/wall_pov_v_r.png'), (tile_width, tile_height)),
    'wall-vert-pov-l': pygame.transform.scale(pygame.image.load('data/wall_pov_v_l.png'), (tile_width, tile_height)),
    'wall-nizh-pov-r': pygame.transform.scale(pygame.image.load('data/wall_pov_n_r.png'), (tile_width, tile_height)),
    'wall-nizh-pov-l': pygame.transform.scale(pygame.image.load('data/pov_n_l.png'), (tile_width, tile_height)),
    'stena_vert': pygame.transform.scale(pygame.image.load('data/wall_vert.png'), (tile_width, tile_height)),
    'player_test': pygame.image.load('data/player_test.png')
}


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Empty(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.image = tile_images[tile_type].convert()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.iter = 0
        super().__init__(player_group)
        self.pos_x = 200
        self.pos_y = 200
        self.speed = 50
        self.angle = 0
        self.image = tile_images['player_test'].convert_alpha()
        self.orig = self.image
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        keys = pygame.key.get_pressed()
        pos_x = self.pos_x
        pos_y = self.pos_y
        mx, my = pygame.mouse.get_pos()
        if mx < 100 or mx > width - 100:
            pygame.mouse.set_pos([width // 2, height // 2])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-40, min(40, self.rel))
        self.angle += self.rel * 0.2 * 1
        self.angle %= math.tau
        self.rotate()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        if keys[pygame.K_w]:
            self.pos_x += self.speed * sin_a
            self.pos_y += self.speed * cos_a
        if keys[pygame.K_s]:
            self.pos_y += self.speed / 200
        if keys[pygame.K_d]:
            self.pos_x += self.speed / 200
        if keys[pygame.K_a]:
            self.pos_x -= self.speed / 200
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                if self.pos_y != pos_y:
                    self.pos_y = pos_y
                if self.pos_x != pos_x:
                    self.pos_x = pos_x
                self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))


svobod = []
tick = 0


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Empty('empty', x + 0.5, y + 0.5)
            if level[y][x] == 'g':
                Wall('wall-gor', x + 0.5, y + 0.5)
            if level[y][x] == 'v':
                Wall('wall-vert', x + 0.5, y + 0.5)
            if level[y][x] == 'q':
                Wall('wall-vert-pov-r', x + 0.5, y + 0.5)
            if level[y][x] == 'e':
                Wall('wall-vert-pov-l', x + 0.5, y + 0.5)
            if level[y][x] == 'w':
                Wall('wall-nizh-pov-r', x + 0.5, y + 0.5)
            if level[y][x] == 'r':
                Wall('wall-nizh-pov-l', x + 0.5, y + 0.5)
            if level[y][x] == '#':
                Wall('stena_vert', x + 0.5, y + 0.5)
            if level[y][x] == '@':
                Empty('empty', x + 0.5, y + 0.5)


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    empty_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    level_map = Map()
    generate_level(level_map.load_level())
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 15, bold=True)
    screen = pygame.display.set_mode(size)
    new_player = Player()
    background = pygame.image.load('data/background.jpg')
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                count = 0
        new_player.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.flip()
        clock.tick(60)
