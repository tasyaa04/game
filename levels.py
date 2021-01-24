import pygame
from images import *
from obstacles import *


WIDTH, HEIGHT = 1280, 750   # размер экрана можно поменять


class Level():
    def __init__(self):
        self.platforms = pygame.sprite.Group()  # создаем группу для платформ
        self.enemies = pygame.sprite.Group()    # и врагов
        self.background = get_images('Background', '.png')

        self.shift = 0

    def draw(self, screen):    # отрисовка уровня
        background = pygame.transform.scale(self.background[0], (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        
    def update(self):
        self.platforms.update()
        self.enemies.update()

    def scroll(self, shift):
        self.shift += shift
        possible_left_shift = -min([platform.rect.x for platform in self.platforms])
        possible_right_shift = WIDTH - max([platform.rect.x for platform in self.platforms])

        if self.shift <= possible_left_shift:
            self.shift -= possible_left_shift
        elif self.shift >= possible_right_shift:
            self.shift -= possible_right_shift

        # т. о. при перемещении игрока вправо/влево положение платформ/врагов тоже менятеся
        for platform in self.platforms:
            platform.rect.x += shift
        for enemy in self.enemies:
            enemy.rect.x += shift


class Level1(Level):   # это незаконченный первый уровень
    def __init__(self):
        super().__init__()

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
                 ['Grass', '.png', 300, 400],
                 ['Grass', '.png', 428, 400],
                 ['Grass', '.png', 640, 450],
                 ['Grass', '.png', 800, 335],
                 ]    # создаем список платформ ex: [image_name, format_name, x, y]

        for i in level:
            platform = Platform(i[0], i[1])
            platform.rect.x, platform.rect.y = i[2], i[3]
            self.platforms.add(platform)

        platform = MovingPlatform('Grass', '.png')
        platform.set_speed(1, 1)
        platform.rect.x, platform.rect.y = 960, 470
        platform.set_borders(900, 960, 470, 598)
        platform.level = self
        self.platforms.add(platform)
