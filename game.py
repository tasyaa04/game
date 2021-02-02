import pygame
import os
import sys

from player import Player
from levels import Level2
from game_over import game_over


def main():
    pygame.init()
    pygame.mixer.pre_init(frequency=44100, size=1024, channels=2, buffer=512)
    music = pygame.mixer.Sound('sfx/MUS_AviaryAction.wav')
    music.set_volume(0.3)
    music.play(-1)
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    active_group = pygame.sprite.Group()

    player = Player()
    active_group.add(player)
    level = Level2(player)
    player.level = level
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        level.update()
        active_group.update()

        if player.rect.x >= 960 and level.allow_right:
            shift = player.rect.x - 960
            level.scroll(-shift)
            player.rect.x = 960
        if player.rect.x <= 960 and level.allow_left:
            shift = 960 - player.rect.x
            level.scroll(shift)
            player.rect.x = 960 

        if not player.running:
            if not game_over(screen):
                running = False
            else:
                player.running = True
                shift = -level.shift
                level.scroll(shift)
                player.rect.bottom, player.rect.centerx = level.beginning[1], level.beginning[0]

        level.draw(screen)
        active_group.draw(screen)
        player.bullets.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
