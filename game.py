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

    list_of_levels = [Level1()]  # список со всеми уровнями
    current_level = list_of_levels[0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    #    current_level.update()
        current_level.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
