import pygame
from images import *
from obstacles import *


WIDTH, HEIGHT = 800, 400    # размер экрана можно поменять


class Level():
    def __init__(self, player):
        self.player = player
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
    def __init__(self, player):
        super().__init__(player)

        level = [['Dirt', '.png', 400, 200]]    # создаем список платформ ex: [image_name, format_name, x, y]

        for i in level:
            platform = Platform(i[0], i[1])
            platform.rect.x, platform.rect.y = i[2], i[3]