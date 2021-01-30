import pygame
from images import *
from obstacles import *
from player import *

WIDTH, HEIGHT = 1920, 1080  # размер экрана можно поменять


class Level():
    def __init__(self, player):
        self.platforms = pygame.sprite.Group()  # создаем группу для платформ
        self.enemies = pygame.sprite.Group()  # и врагов
        self.background = get_images('Background', '.png')

        self.shift = 0
        self.player = player
        self.scroll_limit = 0
        self.possible_left_shift = self.player.rect.x
        self.possible_right_shift = self.scroll_limit

    def draw(self, screen):  # отрисовка уровня
        background = pygame.transform.scale(self.background[0], (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        self.platforms.draw(screen)
        self.enemies.draw(screen)

    def update(self):
        self.platforms.update()
        self.enemies.update()

    def scroll(self, shift):
        if shift > 0:
            if shift <= self.possible_right_shift:
                self.shift += shift
                self.possible_right_shift -= shift
            else:
                self.shift -= self.possible_right_shift
        elif shift < 0:
            if shift >= self.possible_left_shift:
                self.shift += shift
                self.possible_left_shift -= shift
            else:
                self.shift -= self.possible_left_shift


class Level1(Level):  # это незаконченный первый уровень
    def __init__(self, player):
        super().__init__(player)

        level = [['Grass', '.png', 0, 650],
                 ['Grass', '.png', 128, 650],
                 ['Grass', '.png', 256, 650],
                 ['Grass', '.png', 384, 650],
                 ['Grass', '.png', 512, 650],
                 ['Grass', '.png', 640, 650],
                 ['Grass', '.png', 768, 650],
                 ['Grass', '.png', 896, 650],
                 ['Grass', '.png', 896 + 128, 650],
                 ['Grass', '.png', 896 + 256, 650],
                 ['Grass', '.png', 896 + 256 + 128, 650],
                 ['Grass', '.png', 1408, 650],
                 ['Grass', '.png', 1536, 650],
                 ['Grass', '.png', 300, 400],
                 ['Grass', '.png', 428, 400],
                 ['Grass', '.png', 640, 450],
                 ['Grass', '.png', 800, 335],
                 ]  # создаем список платформ ex: [image_name, format_name, x, y]

        self.scroll_limit = 256

        for i in level:
            platform = Platform(i[0], i[1])
            platform.rect.x, platform.rect.y = i[2], i[3]
            self.platforms.add(platform)

        platform = MovingPlatform('Grass', '.png')
        platform.set_speed(1, 1)
        platform.rect.x, platform.rect.y = 960, 470
        platform.set_borders(900, 960, 470, 598)
        platform.level = self
        platform.player = self.player
        self.platforms.add(platform)
