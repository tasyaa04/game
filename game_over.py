import pygame

from levels import WIDTH, HEIGHT
from images import load_image


def game_over(screen):
    background = pygame.transform.scale(load_image('gameOver.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(50)
