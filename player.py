"""Module used to interact with player"""

import pygame
import os
from images import get_images


class Player(pygame.sprite.Sprite):
    """Class of the player that user controls"""

    def __init__(self, level, *groups):
        super().__init__(*groups)

        # direction that player is facing
        self.player_facing = 'r'

        # all animation for player including directions
        self.idle_r = get_images(f'Idle{os.sep}cuphead_idle_0001...0005')
        self.idle_l = [pygame.transform.flip(img, True, False) for img in self.idle_r]
        self.run_normal_r = get_images(f'Run{os.sep}Normal{os.sep}cuphead_run_0001...00016')
        self.run_normal_l = [pygame.transform.flip(img, True, False) for img in self.run_normal_r]
        self.run_shoot_r = get_images(f'Run{os.sep}Shooting{os.sep}cuphead_run_shoot_0001...00016')
        self.run_shoot_l = [pygame.transform.flip(img, True, False) for img in self.run_shoot_r]
        self.shoot_r = get_images(f'Shoot{os.sep}cuphead_shoot_straight_0001...0003')
        self.shoot_l = [pygame.transform.flip(img, True, False) for img in self.shoot_r]
        self.jump_r = get_images(f'Jump{os.sep}Cuphead{os.sep}cuphead_jump_0001...0008')
        self.jump_l = [pygame.transform.flip(img, True, False) for img in self.jump_r]

        # current list of images
        self.current_animation = self.idle_r

        self.image = self.current_animation[0]
        self.rect = self.image.get_rect()

        # speed of player
        self.speed_x = 0
        self.speed_y = 0

        self.level = level
        self.lives = 3

    def update(self):
        """Move the player"""

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        sprites = pygame.sprite.spritecollide(self, self.level.platforms, False)
        if not sprites:
            self.speed_y -= 30
        else:
            self.rect.bottom = sprites[0].rect.top

        # if the player hits the enemies he lose one live
        if pygame.sprite.spritecollide(self, self.level.enemies, False):
            self.lives -= 1
            # if the lives are less than one, game is over
            if self.lives < 1:
                running = False

        self.speed_y = 0

        self.update_animation()

    def update_animation(self):
        keys = pygame.key.get_pressed()

        # changing direction of player
        if keys[pygame.K_LEFT]:
            self.player_facing = 'l'
        elif keys[pygame.K_RIGHT]:
            self.player_facing = 'r'

        # changing animation depending on pressed keys
        if keys[pygame.K_UP] or not pygame.sprite.spritecollide(self, self.level.platforms, False):
            self.current_animation = self.jump_r if self.player_facing == 'r' else self.jump_l
        elif keys[pygame.K_SPACE] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.current_animation = self.run_shoot_r \
                if self.player_facing == 'r' else self.run_shoot_l
        elif keys[pygame.K_SPACE] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.current_animation = self.shoot_r if self.player_facing == 'r' else self.shoot_l
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.current_animation = self.run_normal_r \
                if self.player_facing == 'r' else self.run_normal_l
        else:
            self.current_animation = self.idle_r if self.player_facing == 'r' else self.idle_l

        # changing frame of animation
        try:
            self.image = self.current_animation[(self.current_animation.index(self.image) + 1) %
                                                len(self.current_animation)]
        except IndexError:
            self.image = self.current_animation[0]