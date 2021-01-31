import pygame
import os
import sys
from levels import *
from player import *


def main():     # основной цикл программы
    pygame.init()
    size = WIDTH, HEIGHT    # константы из модуля levels, там их значения можно поменять
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Platformer')

    active_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    player = Player()

    active_group.add(player)

    list_of_levels = [Level1(player),
                      Level2(player)]  # список со всеми уровнями
    current_level = list_of_levels[1]
    player.level = current_level

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        current_level.update()
        active_group.update()

        if player.rect.x >= 960 and current_level.allow_right:
            shift = player.rect.x - 960
            current_level.scroll(-shift)
            player.rect.x = 960
        if player.rect.x <= 960 and current_level.allow_left:
            shift = 960 - player.rect.x
            current_level.scroll(shift)
            player.rect.x = 960

        current_level.draw(screen)
        active_group.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
