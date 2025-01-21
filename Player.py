import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, tile_width, tile_height, svobod, tick, tile_images):
        self.iter = 0
        super().__init__(player_group, all_sprites)
        self.pos_x = 200
        self.pos_y = 200
        self.frames = []
        self.svobod = svobod
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tick = tick
        self.cur_frame = 0
        self.image = tile_images['player_test']
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)
        self.speed = 10


    def update(self, move):
        if move:
            p_x = self.pos_x
            p_y = self.pos_y

            if move == 1:
                self.pos_x -= self.speed
            elif move == 2:
                self.pos_x += self.speed
            elif move == 3:
                self.pos_y -= self.speed
            elif move == 4:
                self.pos_y += self.speed
            if (self.pos_x, self.pos_y) in self.svobod:
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.pos_y)
            else:
                self.pos_x = p_x
                self.pos_y = p_y
