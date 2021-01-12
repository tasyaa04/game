import pygame
import os
import sys


def main():
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
