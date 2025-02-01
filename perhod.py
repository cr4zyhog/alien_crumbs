import pygame

tile_width = tile_height = 75

tile_images = {
    'stone': pygame.transform.scale(pygame.image.load('data/Space/Stone/stone.png'), (tile_width, tile_height)),
    'alien': pygame.transform.scale(pygame.image.load('data/Space/alien/alien_ship.png'), (tile_width, tile_height))
}

alien_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

class Stone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(stone_group)
        self.image = tile_images[tile_type]
        self.angle = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.angle += 10
        self.image = pygame.transform.rotate(self.image.get_rect().move(self.rect.x, self.rect.y), self.angle)
        self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y + dvizh))


class Alien(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(alien_group)
        self.image = tile_images[tile_type]
        self.angle = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y + dvizh))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.pos_x = 787
        self.pos_y = 750
        self.image = pygame.transform.rotate(tile_images['ship'], angle / 57)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.count_time = 1

    def update(self):
        self.pos_y += (10 / clock.get_fps()) * (self.count_time / clock.get_fps())
        alien_group.update((10 / clock.get_fps()) * (self.count_time / clock.get_fps()))
        stone_group.update((10 / clock.get_fps()) * (self.count_time / clock.get_fps()))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= 75
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += 75



def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 's':
                Stone('stone', x + 10, y + 10)
            if level[y][x] == 'a':
                Stone('alien', x + 10, y + 10)
