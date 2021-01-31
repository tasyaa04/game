from obstacles import *
from player import *

WIDTH, HEIGHT = 1920, 1080  # размер экрана можно поменять


class Level:
    def __init__(self, player):
        self.platforms = pygame.sprite.Group()  # создаем группу для платформ
        self.enemies = pygame.sprite.Group()  # и врагов
        self.environment = pygame.sprite.Group()
        self.background = get_images('Background', '.png')

        self.shift = 0
        self.player = player
        self.scroll_limit = 0
        self.possible_left_shift = self.player.rect.x
        self.possible_right_shift = self.scroll_limit

        self.allow_left = False
        self.allow_right = True

    def draw(self, screen):  # отрисовка уровня
        background = pygame.transform.scale(self.background[0], (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.environment.draw(screen)

    def update(self):
        self.platforms.update()
        self.enemies.update()
        self.environment.update()

    def scroll(self, shift):
        self.shift += shift
        self.allow_left = True if self.shift < self.possible_left_shift else False
        self.allow_right = True if abs(self.shift) < self.possible_right_shift else False
        for i in self.environment:
            i.rect.x += shift

        for platform in self.platforms:
            platform.rect.x += shift
            if platform.__class__.__name__ == 'MovingPlatform':
                borders = platform.border_left, platform.border_right, platform.border_bottom, \
                          platform.border_top
                platform.set_borders(*[x + shift for x in borders])


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

        self.possible_right_shift = 500

        for i in level:
            platform = Platform(i[0], i[1])
            platform.rect.x, platform.rect.y = i[2], i[3]
            self.platforms.add(platform)

        platform = MovingPlatform('Grass', '.png')
        platform.set_speed(10, 10)
        platform.rect.x, platform.rect.y = 960, 470
        platform.set_borders(900, 1800, 470, 598)
        platform.level = self
        platform.player = self.player
        self.platforms.add(platform)


class Level2(Level):
    def __init__(self, player):
        super().__init__(player)

        level = [['Grass', '.png', 0, 600],
                 ['Grass', '.png', 128, 600],
                 ['Dirt', '.png', 0, 728],
                 ['Dirt', '.png', 128, 728],
                 ['Dirt', '.png', 128, 856],
                 ['Dirt', '.png', 128, 984],
                 ['Dirt', '.png', 0, 856],
                 ['Dirt', '.png', 0, 984],
                 ['Grass', '.png', 256, 600],
                 ['Dirt', '.png', 256, 728],
                 ['Dirt', '.png', 256, 856],
                 ['Dirt', '.png', 256, 984],
                 ['Grass', '.png', 384, 756],
                 ['Grass', '.png', 512, 756],
                 ['Grass', '.png', 640, 756],
                 ['Dirt', '.png', 384, 884],
                 ['Dirt', '.png', 512, 884],
                 ['Dirt', '.png', 640, 884],
                 ['Dirt', '.png', 384, 1012],
                 ['Dirt', '.png', 512, 1012],
                 ['Dirt', '.png', 640, 1012],
                 ['Grass', '.png', 850, 556],
                 ['Grass', '.png', 978, 556],
                 ['Grass', '.png', 996, 900],
                 ['Grass', '.png', 1124, 900],
                 ['Grass', '.png', 1252, 900],
                 ['Grass', '.png', 1380, 900],
                 ['Grass', '.png', 1200, 360],
                 ['Grass', '.png', 1328, 360],
                 ['Grass', '.png', 1456, 360],
                 ['Grass', '.png', 2400, 590],
                 ['Grass', '.png', 2528, 590],
                 ['Grass', '.png', 2908, 390],
                 ['Grass', '.png', 3036, 390],
                 ['Grass', '.png', 3164, 390],
                 ['Grass', '.png', 3008, 800],
                 ['Grass', '.png', 2880, 800],
                 ['Grass', '.png', 2752, 800],
                 ['Grass', '.png', 3400, 600],
                 ['Grass', '.png', 3528, 600],
                 ['Grass', '.png', 3656, 600],
                 ['Dirt', '.png', 3656, 728],
                 ['Dirt', '.png', 3656, 856],
                 ['Dirt', '.png', 3656, 984],
                 ['Dirt', '.png', 3528, 728],
                 ['Dirt', '.png', 3528, 856],
                 ['Dirt', '.png', 3528, 984],
                 ['Dirt', '.png', 3400, 728],
                 ['Dirt', '.png', 3400, 856],
                 ['Dirt', '.png', 3400, 984],
                 ]  # создаем список платформ ex: [image_name, format_name, x, y]

        self.possible_right_shift = 1975

        environment = [
            [f'Environment{os.sep}Asset 8', '.png', 135, 580],
            [f'Environment{os.sep}Asset 1', '.png', 1300, 659],
            [f'Environment{os.sep}Asset 9', '.png', 1290, 890],
            [f'Environment{os.sep}Asset 6', '.png', 1350, 885],
            [f'Environment{os.sep}Asset 13', '.png', 246, 585],
            [f'Environment{os.sep}Asset 15', '.png', 650, 748],
            [f'Environment{os.sep}Asset 6', '.png', 900, 540],
            [f'Environment{os.sep}Asset 2', '.png', 3600, 355],
            [f'Environment{os.sep}Asset 6', '.png', 3610, 580],
            [f'Environment{os.sep}Asset 6', '.png', 3000, 780],
            [f'Environment{os.sep}Asset 11', '.png', 2990, 788],
        ]

        for i in level:
            platform = Platform(i[0], i[1])
            platform.rect.x, platform.rect.y = i[2], i[3]
            self.platforms.add(platform)

        for i in environment:
            sprite = pygame.sprite.Sprite()
            sprite.image = get_images(i[0], i[1])[0]
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x, sprite.rect.y = i[2], i[3]
            self.environment.add(sprite)

        platform = MovingPlatform('Grass', '.png')
        platform.set_speed(10, 0)
        platform.rect.x, platform.rect.y = 1800, 470
        platform.set_borders(1800, 2200, 470, 598)
        platform.level = self
        platform.player = self.player
        self.platforms.add(platform)


