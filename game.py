import pygame
import os
import sys
from levels import *


def main():     # основной цикл программы
    pygame.init()
    size = WIDTH, HEIGHT    # константы из модуля levels, там их значения можно поменять
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Platformer')

    levels = []     # список со всеми уровнями

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
