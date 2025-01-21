import pygame

from map import Map
from Player import Player

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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


svobod = []
tick = 0

def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x + 0.5, y + 0.5)
                svobod.append((x, y))
            if level[y][x] == 'g':
                Tile('wall-gor', x + 0.5, y + 0.5)
            if level[y][x] == 'v':
                Tile('wall-vert', x + 0.5, y + 0.5)
            if level[y][x] == 'q':
                Tile('wall-vert-pov-r', x + 0.5, y + 0.5)
            if level[y][x] == 'e':
                Tile('wall-vert-pov-l', x + 0.5, y + 0.5)
            if level[y][x] == 'w':
                Tile('wall-nizh-pov-r', x + 0.5, y + 0.5)
            if level[y][x] == 'r':
                Tile('wall-nizh-pov-l', x + 0.5, y + 0.5)
            if level[y][x] == '#':
                Tile('stena_vert', x + 0.5, y + 0.5)
            if level[y][x] == '@':
                Tile('empty', x + 0.5, y + 0.5)
                p_x = x * tile_width
                p_y = y * tile_height


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    level_map = Map()
    generate_level(level_map.load_level())
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1920, 1080

    screen = pygame.display.set_mode(size)
    new_player = Player(player_group, all_sprites, tile_width, tile_height, svobod, tick, tile_images)
    screen.fill((0, 0, 0))
    flg = False
    while True:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                count = 0
                flg = True
            elif event.type == pygame.KEYUP:
                flg = False
        if flg:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_group.update(1)
            if keys[pygame.K_RIGHT]:
                player_group.update(2)
            if keys[pygame.K_UP]:
                player_group.update(3)
            if keys[pygame.K_DOWN]:
                player_group.update(4)
        screen.blit(pygame.image.load('data/background.jpg'), (0, 0))
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
