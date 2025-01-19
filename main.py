import pygame
from map import Map

tile_width = tile_height = 10
tile_images = {
    'empty': pygame.transform.scale(pygame.image.load('pol.jpg'), (tile_width, tile_height))
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
level_map = Map()
generate_level(level_map.load_level())
pygame.init()
size = width, height = 1280, 720

screen = pygame.display.set_mode(size)
screen.fill((0, 0 ,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    all_sprites.draw(screen)
    pygame.display.flip()
