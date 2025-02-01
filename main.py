import random
from itertools import count
import pygame
import math
import perhod
from pygame import MOUSEBUTTONDOWN
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
    'wall_t_r': pygame.transform.scale(pygame.image.load('data/Wall_T_r.png'), (tile_width, tile_height)),
    'wall_t_l': pygame.transform.scale(pygame.image.load('data/Wall_T_l.png'), (tile_width, tile_height)),
    'wall_end_up': pygame.transform.scale(pygame.image.load('data/wall_end_up.png'), (tile_width, tile_height)),
    'wall_end_down': pygame.transform.scale(pygame.image.load('data/wall_end_down.png'), (tile_width, tile_height)),
    'wall_t_u': pygame.transform.scale(pygame.image.load('data/Wall_T_u.png'), (tile_width, tile_height)),
    'wall_t_d': pygame.transform.scale(pygame.image.load('data/Wall_T_d.png'), (tile_width, tile_height)),
    'wall_end_r': pygame.transform.scale(pygame.image.load('data/wall_end_r.png'), (tile_width, tile_height)),
    'wall_end_l': pygame.transform.scale(pygame.image.load('data/wall_end_l.png'), (tile_width, tile_height)),
    'box_green': pygame.transform.scale(pygame.image.load('data/box_green.png'), (tile_width, tile_height)),
    'box': pygame.transform.scale(pygame.image.load('data/box.png'), (tile_width, tile_height)),
    'cont': pygame.transform.scale(pygame.image.load('data/container.png'), (tile_width, tile_height))
}

weapons_images = {
    'pistol': pygame.image.load('data/weapons/pistol.png').convert_alpha(),
    'avtomat': pygame.image.load('data/weapons/avtomat.png').convert_alpha(),
    'pulemet': pygame.image.load('data/weapons/pulemet.png').convert_alpha(),
    'rpg': pygame.image.load('data/weapons/rpg.png').convert_alpha(),
}

alien_images = [pygame.image.load('data/aliens/alien1/alien_1.png').convert_alpha(),
                pygame.image.load('data/aliens/alien1/alien_2.png').convert_alpha(),
                pygame.image.load('data/aliens/alien1/alien_hit.png').convert_alpha()]

bullets_images = [pygame.image.load('data/bullets/pistol_bullet.png').convert_alpha(),
                  pygame.image.load('data/bullets/avtomat_bullet.png').convert_alpha()]

player_imges = {
    'pistol': [pygame.image.load('data/data_player/player_with_pistol/pistol0.png').convert_alpha(),
               pygame.image.load('data/data_player/player_with_pistol/pistol1.png').convert_alpha()],
    'avtomat': [pygame.image.load('data/data_player/player_with_avtomat/avto0.png').convert_alpha(),
                pygame.image.load('data/data_player/player_with_avtomat/avto1.png').convert_alpha()],
    'pulemet': [pygame.image.load('data/data_player/player_with_pulemet/pule0.png').convert_alpha(),
                pygame.image.load('data/data_player/player_with_pulemet/pule1.png').convert_alpha()],
    'rpg': [pygame.image.load('data/data_player/player_with_pulemet/pule0.png').convert_alpha(),
            pygame.image.load('data/data_player/player_with_pulemet/pule1.png').convert_alpha()],
    'die': [pygame.image.load('data/data_player/player_die/die_0.png').convert_alpha(),
            pygame.image.load('data/data_player/player_die/die_1.png').convert_alpha(),
            pygame.image.load('data/data_player/player_die/die_2.png').convert_alpha(),
            pygame.image.load('data/data_player/player_die/die_3.png').convert_alpha()]
}

sounds = {
    'weapon': pygame.mixer.Sound('data/sounds/bullet.mp3'),
    'wall': pygame.mixer.Sound('data/sounds/bullet_wall.mp3'),
    'alien_hit': pygame.mixer.Sound('data/sounds/alien_hit.mp3'),
    'see_player': pygame.mixer.Sound('data/sounds/see_player.mp3'),
    'alien_death': pygame.mixer.Sound('data/sounds/alien_death.mp3'),
    'monsterkill': pygame.mixer.Sound('data/sounds/announcer_kill_monster_01_1.mp3'),
    'player_oogh': pygame.mixer.Sound('data/sounds/player_oogh.mp3'),
    'player_die': pygame.mixer.Sound('data/sounds/player_death.mp3')
}

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 250)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(weapon_group)
        self.image = weapons_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.rect = self.image.get_rect().move(self.rect.x - dvizh, self.rect.y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.rect = self.image.get_rect().move(self.rect.x - dvizh, self.rect.y)


class Empty(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.image = tile_images[tile_type].convert()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.rect = self.image.get_rect().move(self.rect.x - dvizh, self.rect.y)


see_player_music = False


class Aliens(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy):
        super().__init__(aliens_group)
        self.image = alien_images[0]
        self.vel = pygame.math.Vector2((0, 0))
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        pygame.mixer.music.load('data/sounds/see_player.mp3')
        self.death_sound = sounds['alien_death']
        self.hit_sound = sounds['alien_hit']
        self.hp = 100
        self.angle = 0
        self.last_hit = 0
        self.alive = True
        self.in_hit = False
        self.in_hit_count = 0
        self.speed_x = vx
        self.speed_y = vy
        self.count = 0
        self.see_player = False
        self.last_seen_player = 0
        self.rect = self.image.get_rect(center=pos)
        self.rect_orig = self.image.get_rect()
        self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect_orig.width - 2 * 4,
                                       self.rect_orig.height - 2 * 4)
        self.hitbox.center = self.rect_orig.center

    def update(self, flag=False):
        if self.in_hit:
            if self.in_hit_count > 5:
                self.in_hit = False
                self.image = alien_images[0]
                self.in_hit_count = 0
            self.in_hit_count += 1
        pos_x = self.pos.x
        if pos_x >= 2300 or pos_x <= -380:
            return 0
        if flag:
            self.update_image()
        if self.count == 75:
            self.speed_x, self.speed_y = -self.speed_x, -self.speed_y
            self.count = 0
        self.look_for_player()
        if not self.see_player:
            self.acc = pygame.math.Vector2(0, 0)
            self.vel.x += self.speed_x
            self.vel.y += self.speed_y
            self.count += 1
        else:
            self.acc = pygame.math.Vector2(0, 0)
            pos_x = new_player.rect.centerx
            pos_y = new_player.rect.centery
            player_vec = pygame.math.Vector2(pos_x, pos_y)
            sin_a = math.sin(self.angle)
            cos_a = math.cos(self.angle)
            speed = new_player.speed
            if player_vec.x > self.pos.x:
                self.vel.x += speed
            if player_vec.x < self.pos.x:
                self.vel.x -= speed
            if player_vec.y > self.pos.y:
                self.vel.y += speed
            if player_vec.y < self.pos.y:
                self.vel.y -= speed

        self.acc += self.vel * -0.47
        self.vel += self.acc
        if self.vel.x != 0:
            self.pos.x += round(self.vel.x + 0.5 * self.acc.x, 1)
            self.hitbox.center = self.pos
            self.check_collision('x')

        if self.vel.y != 0:
            self.pos.y += round(self.vel.y + 0.5 * self.acc.y, 1)
            self.hitbox.center = self.pos
            self.check_collision('y')

        self.rect.center = self.pos

        if self.hitbox.colliderect(new_player.rect):
            if pygame.time.get_ticks() - self.last_hit >= 400:
                if new_player.armor > 0:
                    new_player.armor -= 10
                    new_player.player_oogh.play()
                    self.last_hit = pygame.time.get_ticks()
                else:
                    new_player.hp -= 10
                    new_player.player_oogh.play()
                    self.last_hit = pygame.time.get_ticks()
                if new_player.hp <= 0:
                    new_player.die()

    def check_collision(self, axis):
        for wall in wall_group:
            if axis == 'x':
                if abs(wall.rect.centerx - self.pos.x) < 100:
                    if self.hitbox.colliderect(wall):
                        if self.vel.x < 0:
                            self.hitbox.left = wall.rect.right
                        elif self.vel.x > 0:
                            self.hitbox.right = wall.rect.left
                        self.pos.x = self.hitbox.centerx
            else:
                if abs(wall.rect.centery - self.pos.y) < 100:
                    if self.hitbox.colliderect(wall):
                        if self.vel.y < 0:
                            self.hitbox.top = wall.rect.bottom
                        elif self.vel.y > 0:
                            self.hitbox.bottom = wall.rect.top
                        self.pos.y = self.hitbox.centery

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
        self.hp = 100
        self.armor = 100
        self.speed = 7
        self.pos_mouse = (0, 0)
        self.angle = 0
        self.last_hit = 0
        self.new_angle = 0
        self.weapon = 'pistol'
        self.gipoten = 0
        self.count = 0
        self.die_count = 0
        self.flag = False
        self.image = player_imges['pistol'][0]
        self.bullet_sound = sounds['weapon']
        self.die_flag = False
        self.player_oogh = sounds['player_oogh']
        self.player_die = sounds['player_die']
        self.image_swap_count = 0
        self.orig = self.image
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self.rect_orig = self.image.get_rect()
        self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect_orig.width - 2 * 4,
                                       self.rect_orig.height - 2 * 4)
        self.hitbox.center = self.rect_orig.center

    def obnov_mish(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self.hitbox.center = (self.pos_x, self.pos_y)

    def update(self):
        if self.die_flag:
            if self.die_count <= 10:
                self.orig = player_imges['die'][0]
            elif self.die_count <= 20:
                self.orig = player_imges['die'][1]
            elif self.die_count <= 30:
                self.orig = player_imges['die'][2]
            elif self.die_count <= 40:
                self.orig = player_imges['die'][3]
            self.die_count += 1
            self.rotate()
            return 0
        keys = pygame.key.get_pressed()
        if self.image_swap_count == 1:
            self.orig = player_imges[self.weapon][1]
            self.image_swap_count = 0
        else:
            self.orig = player_imges[self.weapon][0]
        for w in weapon_group.sprites():
            if self.hitbox.colliderect(w.rect):
                self.weapon = w.type
                w.kill()
        if self.orig != player_imges[self.weapon][0] or self.orig != player_imges[self.weapon][1]:
            self.image = player_imges[self.weapon][0]
            self.orig = player_imges[self.weapon][0]
        angle_orr = self.angle
        self.angle = 0
        self.rotate()
        self.angle = angle_orr
        pos_x = self.pos_x
        pos_y = self.pos_y
        self.update_mouse(pygame.mouse.get_pos())
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0]:
            if self.weapon == 'pistol':
                if pygame.time.get_ticks() - self.count >= 400:
                    self.count = pygame.time.get_ticks()
                    self.flag = not self.flag
                    self.attack()
            elif self.weapon == 'pulemet':
                if pygame.time.get_ticks() - self.count >= 70:
                    self.count = pygame.time.get_ticks()
                    self.flag = not self.flag
                    self.attack()
            elif self.weapon == 'avtomat':
                if pygame.time.get_ticks() - self.count >= 170:
                    self.count = pygame.time.get_ticks()
                    self.flag = not self.flag
                    self.attack()
        if keys[pygame.K_w]:
            # self.gipoten -= self.speed
            self.pos_y -= self.speed
            self.hitbox.center = (self.pos_x, self.pos_y)
        if keys[pygame.K_s]:
            # self.gipoten += self.speed
            self.pos_y += self.speed
            self.hitbox.center = (self.pos_x, self.pos_y)
        if keys[pygame.K_d]:
            # self.angle = (self.angle + (300 / self.gipoten)) % 360
            self.pos_x += self.speed
            self.hitbox.center = (self.pos_x, self.pos_y)
        if keys[pygame.K_a]:
            # self.angle = (self.angle - (300 / self.gipoten)) % 360
            self.pos_x -= self.speed
            self.hitbox.center = (self.pos_x, self.pos_y)
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
        for wall in wall_group.sprites():
            if self.hitbox.colliderect(wall):
                if self.hitbox.right >= wall.rect.left or self.hitbox.left < wall.rect.right:
                    if self.hitbox.right - wall.rect.left > tile_width:
                        self.hitbox.left = wall.rect.right
                        self.pos_x = self.hitbox.centerx
                    elif self.hitbox.right - wall.rect.left < tile_width:
                        self.hitbox.right = wall.rect.left
                        self.pos_x = self.hitbox.centerx
                if self.hitbox.top <= wall.rect.bottom or self.hitbox.bottom > wall.rect.top:
                    if self.hitbox.bottom - wall.rect.top > tile_width:
                        self.hitbox.top = wall.rect.bottom
                        self.pos_y = self.hitbox.centery
                    elif self.hitbox.bottom - wall.rect.top < tile_width:
                        self.hitbox.bottom = wall.rect.top
                        self.pos_y = self.hitbox.centery

        self.rotate()

    def die(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.player_die.play()
        self.die_flag = True

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

    def attack(self):
        self.orig = player_imges[self.weapon][1]
        self.image_swap_count += 1
        self.bullet_sound.play()
        if self.weapon != 'pistol':
            Bullets(0, self.angle, (self.rect.centerx - (7 * math.cos(self.angle / 57.3)), self.rect.centery))
        else:
            Bullets(0, self.angle, self.rect.center)


death_count = 0
tick_from_death = 0


class Bullets(pygame.sprite.Sprite):
    def __init__(self, type, angle, pos):
        super().__init__(bullets_group)
        self.wall_sound = sounds['wall']
        self.angle = angle
        self.count = 0
        self.tick_from_death = 0
        self.death_count = 0
        self.image = pygame.transform.rotate(bullets_images[type], angle / 57)
        self.rect = self.image.get_rect(center=pos)
        self.monsterkill = sounds['monsterkill']

    def update(self):
        global death_count
        global tick_from_death
        # парился с этой фигней два часа, а почему-то нужно было угол поделить на 57
        angle = self.angle / 57.3
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        x = self.rect.centerx
        y = self.rect.centery
        x += (30 * sin_a)
        y += (30 * cos_a)
        self.rect = self.image.get_rect(center=(x, y))
        self.count += 1
        if pygame.sprite.spritecollideany(self, wall_group):
            self.wall_sound.play()
            self.kill()
        for i in aliens_group.sprites():
            if pygame.sprite.collide_mask(self, i):
                i.hit_sound.play()
                i.in_hit = True
                i.image = alien_images[2]
                if new_player.weapon == 'pistol':
                    i.hp -= 10
                elif new_player.weapon == 'avtomat':
                    i.hp -= 25
                elif new_player.weapon == 'pulemet':
                    i.hp -= 20
                i.see_player = True
                i.last_seen_player = pygame.time.get_ticks()
                if i.hp <= 0:
                    if abs(tick_from_death - pygame.time.get_ticks()) <= 2000:
                        death_count += 1
                        if death_count >= 4:
                            self.monsterkill.play()
                        else:
                            i.death_sound.play()
                    else:
                        tick_from_death = pygame.time.get_ticks()
                        i.death_sound.play()
                        death_count = 0
                    i.kill()
                self.kill()


svobod = []
tick = 0


def generate_level(level):
    numbers = range(-1, 2)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Empty('empty', x + 0.5, y + 0.5)
                Weapon('pistol', x + 0.5, y + 0.5)
            if level[y][x] == '1':
                Empty('empty', x + 0.5, y + 0.5)
                Weapon('avtomat', x + 0.5, y + 0.5)
            if level[y][x] == '2':
                Empty('empty', x + 0.5, y + 0.5)
                Weapon('pulemet', x + 0.5, y + 0.5)
            if level[y][x] == '3':
                Empty('empty', x + 0.5, y + 0.5)
                Weapon('rpg', x + 0.5, y + 0.5)
            if level[y][x] == '.':
                Empty('empty', x + 0.5, y + 0.5)
            if level[y][x] == 'A':
                Empty('empty', x + 0.5, y + 0.5)
                vx = random.choice(numbers)
                vy = random.choice(numbers)
                Aliens((x * tile_width, y * tile_height), vx, vy)
            if level[y][x] == 'b':
                Empty('empty', x + 0.5, y + 0.5)
                Wall('box', x + 0.5, y + 0.5)
            if level[y][x] == 'c':
                Empty('empty', x + 0.5, y + 0.5)
                Wall('cont', x + 0.5, y + 0.5)
            if level[y][x] == 'j':
                Empty('empty', x + 0.5, y + 0.5)
                Wall('box_green', x + 0.5, y + 0.5)
            if level[y][x] == 'g':
                Wall('wall-gor', x + 0.5, y + 0.5)
            if level[y][x] == 'n':
                Wall('wall_end_up', x + 0.5, y + 0.5)
            if level[y][x] == 'm':
                Wall('wall_end_down', x + 0.5, y + 0.5)
            if level[y][x] == 'u':
                Wall('wall_t_u', x + 0.5, y + 0.5)
            if level[y][x] == 'i':
                Wall('wall_t_d', x + 0.5, y + 0.5)
            if level[y][x] == 'z':
                Wall('wall_end_l', x + 0.5, y + 0.5)
            if level[y][x] == 'x':
                Wall('wall_end_r', x + 0.5, y + 0.5)
            if level[y][x] == 't':
                Wall('wall_t_r', x + 0.5, y + 0.5)
            if level[y][x] == 'y':
                Wall('wall_t_l', x + 0.5, y + 0.5)
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


def check_press(pos):
    if 200 < pos[0] < 550 and 800 < pos[1] < 900:
        return 'restart'


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    weapon_group = pygame.sprite.Group()
    aliens_group = pygame.sprite.Group()
    empty_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    level_map = Map()
    generate_level(level_map.load_level())
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 20, bold=True)
    font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
    screen = pygame.display.set_mode(size)
    new_player = Player()
    fon = pygame.mixer.Sound('data/sounds/Digiterra — Idle Empyrean (Argent Metal) (www.lightaudio.ru).mp3')
    fon.play(-1)
    new_player.obnov_mish()
    background = pygame.image.load('data/background.jpg')
    screen.blit(background, (0, 0))
    flg_aliens = False
    count_move = 0
    count_die = 0
    game_over = pygame.image.load('data/game_over.png').convert_alpha()
    button_press = ''
    space_flg =
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                count = 0
            if event.type == MYEVENTTYPE:
                flg_aliens = True
            if event.type == MOUSEBUTTONDOWN:
                if new_player.die_flag:
                    button_press = check_press(event.pos)
        if space_flg:

        if new_player.die_flag:
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            new_player.update()
            player_group.draw(screen)
            bullets_group.draw(screen)
            aliens_group.draw(screen)
            if new_player.die_count > 40:
                screen.blit(game_over, (0, 442))
                render = font_game_over.render('Restart', 0, (255, 255, 255))
                screen.blit(render, (200, 800))

                if button_press == 'restart':
                    all_sprites = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    weapon_group = pygame.sprite.Group()
                    aliens_group = pygame.sprite.Group()
                    empty_group = pygame.sprite.Group()
                    wall_group = pygame.sprite.Group()
                    bullets_group = pygame.sprite.Group()
                    level_map = Map()
                    generate_level(level_map.load_level())
                    clock = pygame.time.Clock()
                    font = pygame.font.SysFont('Consolas', 20, bold=True)
                    font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
                    screen = pygame.display.set_mode(size)
                    new_player = Player()
                    fon = pygame.mixer.Sound(
                        'data/sounds/Digiterra — Idle Empyrean (Argent Metal) (www.lightaudio.ru).mp3')
                    fon.play(-1)
                    new_player.obnov_mish()
                    background = pygame.image.load('data/background.jpg')
                    screen.blit(background, (0, 0))
                    flg_aliens = False
                    count_move = 0
                    game_over = pygame.image.load('data/game_over.png').convert_alpha()
                    button_press = ''
        else:
            if count_move == 0:
                if new_player.pos_x >= 1940:
                    count_move = 129
                elif new_player.pos_x <= -20:
                    count_move = -129
            if count_move > 0:
                for alien in aliens_group.sprites():
                    alien.pos.x -= 15
                    alien.rect.center = alien.pos
                wall_group.update(15)
                empty_group.update(15)
                weapon_group.update(15)
                new_player.pos_x -= 15
                count_move -= 1
                screen.blit(background, (0, 0))
            elif count_move < 0:
                for alien in aliens_group.sprites():
                    alien.pos.x += 15
                    alien.rect.center = alien.pos
                wall_group.update(-15)
                empty_group.update(-15)
                weapon_group.update(-15)
                new_player.pos_x += 15
                count_move += 1
                screen.blit(background, (0, 0))
            all_sprites.draw(screen)
            weapon_group.draw(screen)
            new_player.update()
            player_group.draw(screen)
            bullets_group.update()
            bullets_group.draw(screen)
            aliens_group.update(flg_aliens)
            aliens_group.draw(screen)
            pygame.draw.rect(screen, (0, 0, 0), (new_player.rect.centerx - 27, new_player.rect.centery - 35, 54, 10))
            pygame.draw.rect(screen, (200, 0, 0),
                             (new_player.rect.centerx - 25, new_player.rect.centery - 33, new_player.hp / 2, 6))

            pygame.draw.rect(screen, (0, 0, 0), (new_player.rect.centerx - 27, new_player.rect.centery - 45, 54, 10))
            pygame.draw.rect(screen, (200, 200, 200),
                             (new_player.rect.centerx - 25, new_player.rect.centery - 43, new_player.armor / 2, 6))
        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.flip()
        flg_aliens = False
        clock.tick(60)
# assds
