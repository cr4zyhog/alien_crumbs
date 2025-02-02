import pygame
import main
import csv

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


class Menu:
    def __init__(self):
        self.background = pygame.image.load('data/background.png')
        screen.blit(self.background, (0, 0))
        self.font = pygame.font.SysFont('MS Serif', 200, bold=True)
        self.font1 = pygame.font.SysFont('MS Serif', 100, bold=True)
        self.render = 0
        self.level_count = 0
        self.levels = [['levels/level0.txt', 'levels/level0_space.txt'],
                       ['levels/level1.txt', 'levels/level1_space.txt']]
        self.clock = pygame.time.Clock()
        self.button_press = ''

    def update_main_menu(self):
        if self.button_press == 'Exit':
            exit()
        elif self.button_press == 'Play':
            pygame.mixer.stop()
            main.main(self.levels[0], 'pistol')
        elif self.button_press == 'Stats':
            c = 0
            with open('stats.csv', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, i in enumerate(reader):
                    if index == 0:
                        continue
                    self.render = self.font1.render(f'{i[0]}:', 0, (255, 255, 255))
                    screen.blit(self.render, (100, 400 + (100 * c)))
                    self.render = self.font1.render(f'{i[1]}', 0, (255, 255, 255))
                    screen.blit(self.render, (350, 400 + (100 * c)))
                    c += 1
        self.render = self.font.render('Alien Crumbs', 0, (0, 200, 0))
        screen.blit(self.render, (500, 200))
        self.render = self.font1.render('Play', 0, (255, 255, 255))
        screen.blit(self.render, (800, 400))
        self.render = self.font1.render('Stats', 0, (255, 255, 255))
        screen.blit(self.render, (800, 500))
        self.render = self.font1.render('Exit', 0, (255, 255, 255))
        screen.blit(self.render, (800, 600))

    def check_press(self, pos):
        if 800 < pos[0] < 950 and 400 < pos[1] < 475:
            self.button_press = 'Play'
        elif 800 < pos[0] < 980 and 500 < pos[1] < 575:
            self.button_press = 'Stats'
        elif 800 < pos[0] < 950 and 600 < pos[1] < 675:
            self.button_press = 'Exit'

    def check_press_sled(self, pos):
        if 100 < pos[0] < 450 and 800 < pos[1] < 875:
            self.button_press = 'Next level'
        elif 1600 < pos[0] < 1800 and 800 < pos[1] < 875:
            self.button_press = 'Menu'

    def sled_level(self, kills, weapon):
        self.level_count += 1
        pygame.mixer.music.load('data/sounds/fon_menu.mp3')
        pygame.mixer.music.play(-1)
        with open('stats.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for indexx, ii in enumerate(reader):
                if indexx == 0:
                    continue
                if int(ii[1]) < kills and indexx == self.level_count:
                    with open('stats.csv', 'w', newline='', encoding="utf8") as csvvfile:
                        writer = csv.writer(
                            csvvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for index, i in enumerate(reader):
                            if index == 0:
                                continue
                            if i == self.level_count:
                                writer.writerow([f'level{self.level_count - 1}', kills])
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen.blit(self.background, (0, 0))
                        self.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_press_sled(event.pos)
            self.render = self.font.render('Congratulations!', 0, (255, 255, 0))
            screen.blit(self.render, (100, 200))
            self.render = self.font1.render('Kills:', 0, (255, 255, 255))
            screen.blit(self.render, (100, 400))
            self.render = self.font1.render(f'{kills}', 0, (255, 255, 255))
            screen.blit(self.render, (350, 400))
            self.render = self.font1.render('Next level', 0, (255, 255, 255))
            screen.blit(self.render, (100, 800))
            self.render = self.font1.render('Menu', 0, (255, 255, 255))
            screen.blit(self.render, (1600, 800))
            if self.button_press == 'Menu':
                screen.blit(self.background, (0, 0))
                self.run()
            if self.button_press == 'Next level':
                main.main(self.levels[self.level_count], weapon)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        pygame.mixer.music.load('data/sounds/fon_menu.mp3')
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_press(event.pos)
            self.update_main_menu()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    menu = Menu()
    menu.run()
