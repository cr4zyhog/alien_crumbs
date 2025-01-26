import random

import pygame
import math

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

alien_images = [pygame.image.load('data/aliens/alien1/alien_1.png').convert_alpha(),
                pygame.image.load('data/aliens/alien1/alien_2.png').convert_alpha()]

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 250)


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


class Aliens(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy):
        super().__init__(aliens_group)
        self.image = alien_images[0]
        self.vel = pygame.math.Vector2((0, 0))
        self.pos = pos
        self.angle = 0
        self.speed_x = vx
        self.speed_y = vy
        self.count = 0
        self.see_player = False
        self.last_seen_player = 0
        self.rect = self.image.get_rect(center=pos)

    def update(self, flag=False):
        if flag:
            self.update_image()
        if self.count == 75:
            self.speed_x, self.speed_y = -self.speed_x, -self.speed_y
            self.count = 0
        self.look_for_player()
        if not self.see_player:
            self.pos = (self.pos[0] + self.speed_x, self.pos[1] + self.speed_y)
            self.count += 1
            self.rect = self.image.get_rect(center=self.pos)
        else:

            dlin_1 = new_player.pos_y - self.pos[1]
            dlin_2 = new_player.pos_x - self.pos[0]
            gipoten = math.sqrt(dlin_2 ** 2 + dlin_1 ** 2)
            if dlin_2 >= 0:
                try:
                    self.angle = math.acos(dlin_1 / gipoten) * 57.3 % 360
                except ZeroDivisionError:
                    self.angle = 0
            else:
                try:
                    self.angle = 360 - math.acos(dlin_1 / gipoten) * 57.3 % 360
                except ZeroDivisionError:
                    self.angle = 0
            pos_x = new_player.rect.x
            pos_y = new_player.rect.y
            if pos_x > self.pos[0]:
                self.pos = (self.pos[0] + round((new_player.speed * math.sin(self.angle))), self.pos[1])
            if pos_x < self.pos[0]:
                self.pos = (self.pos[0] - round((new_player.speed * math.sin(self.angle))), self.pos[1])
            if pos_y > self.pos[1]:
                self.pos = (self.pos[0], self.pos[1] + round((new_player.speed * math.cos(self.angle))))
            if pos_y < self.pos[1]:
                self.pos = (self.pos[0], self.pos[1] - round((new_player.speed * math.cos(self.angle))))
            self.rect = self.image.get_rect(center=self.pos)

    def look_for_player(self):
        if abs(self.pos[0] - new_player.pos_x) <= 200 and abs(self.pos[1] - new_player.pos_y) <= 200:
            self.last_seen_player = pygame.time.get_ticks()
            self.see_player = True
        elif self.last_seen_player + 2000 < pygame.time.get_ticks():
            self.see_player = False

    def update_image(self):
        if self.image == alien_images[0]:
            self.image = alien_images[1]
        else:
            self.image = alien_images[0]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.pos_x = 400
        self.rel = 0
        self.pos_y = 200
        self.speed = 7
        self.pos_mouse = (0, 0)
        self.angle = 0
        self.new_angle = 0
        self.gipoten = 0
        self.image = tile_images['player_test'].convert_alpha()
        self.orig = self.image
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))

    def obnov_mish(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))

    def update(self):
        keys = pygame.key.get_pressed()
        self.new_angle = self.angle
        pos_x = self.pos_x
        pos_y = self.pos_y
        if keys[pygame.K_w]:
        # self.gipoten -= self.speed
            self.pos_y += self.speed
        if keys[pygame.K_s]:
        # self.gipoten += self.speed
            self.pos_y -= self.speed
        if keys[pygame.K_d]:
        # self.angle = (self.angle + (300 / self.gipoten)) % 360
            self.pos_x += self.speed
        if keys[pygame.K_a]:
        # self.angle = (self.angle - (300 / self.gipoten)) % 360
            self.pos_x -= self.speed
        if keys[pygame.K_UP]:
            self.mouse_pos = (self.mouse_pos[0], self.mouse_pos[1] - self.speed)
            self.update_mouse(self.mouse_pos)
        if keys[pygame.K_DOWN]:
            self.mouse_pos = (self.mouse_pos[0], self.mouse_pos[1] + self.speed)
            self.update_mouse(self.mouse_pos)
        if keys[pygame.K_LEFT]:
            self.mouse_pos = (self.mouse_pos[0] - self.speed, self.mouse_pos[1])
            self.update_mouse(self.mouse_pos)
        if keys[pygame.K_RIGHT]:
            self.mouse_pos = (self.mouse_pos[0] + self.speed, self.mouse_pos[1])
            self.update_mouse(self.mouse_pos)
        # center = (pygame.math.Vector2(self.mouse_pos) + pygame.math.Vector2(0, -self.gipoten).rotate(-self.angle))
        # print(center.angle_to(pygame.math.Vector2(self.mouse_pos)))
        # self.rect = self.image.get_rect(center=(round(abs(center.x)), round(abs(center.y))))
        # pygame.draw.line(screen, (255, 0, 0), (0, 0), (self.mouse_pos[0], self.mouse_pos[1]))
        # pygame.draw.line(screen, (0, 255, 0), (0, 0), (pygame.math.Vector2(10, -self.gipoten).rotate(-self.angle).x, pygame.math.Vector2(10, -self.gipoten).rotate(-self.angle).y))
        # pygame.draw.line(screen, (0, 0, 255), (0, 0), (center.x, center.y))
        self.rotate()

    def update_mouse(self, mouse_pos):
        self.mouse_pos = mouse_pos
        dlin_1 = mouse_pos[1] - self.pos_y
        dlin_2 = mouse_pos[0] - self.pos_x
        self.gipoten = math.sqrt(dlin_2 ** 2 + dlin_1 ** 2)
        if dlin_2 >= 0:
            try:
                self.angle = math.acos(dlin_1 / self.gipoten) * 57.3 % 360
            except ZeroDivisionError:
                self.angle = 0
        else:
            try:
                self.angle = 360 - math.acos(dlin_1 / self.gipoten) * 57.3 % 360
            except ZeroDivisionError:
                self.angle = 0


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


def create_alien():
    aliens_count = 10
    numbers = range(-1, 2)
    x = 150
    for i in range(aliens_count):
        vx = random.choice(numbers)
        vy = random.choice(numbers)
        Aliens((x, 650), vx, vy)
        x += 90


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    aliens_group = pygame.sprite.Group()
    empty_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    level_map = Map()
    create_alien()
    generate_level(level_map.load_level())
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 15, bold=True)
    screen = pygame.display.set_mode(size)
    new_player = Player()
    new_player.obnov_mish()
    background = pygame.image.load('data/background.jpg')
    screen.blit(background, (0, 0))
    flg_aliens = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                count = 0
            if event.type == pygame.MOUSEMOTION:
                new_player.update_mouse(event.pos)
            if event.type == MYEVENTTYPE:
                flg_aliens = True
        all_sprites.draw(screen)
        new_player.update()
        player_group.draw(screen)
        aliens_group.update(flg_aliens)
        aliens_group.draw(screen)
        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.flip()
        flg_aliens = False
        clock.tick(60)
