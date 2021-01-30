"""Module used to interact with player"""

import pygame
import os
from images import get_images


class Player(pygame.sprite.Sprite):
    """Class of the player that user controls"""

    def __init__(self, *groups):
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

        self.level = None
        self.lives = 3

        # used to manage interacting with the platforms
        self.in_air = False
        self.in_fall = True
        self.in_air_secs = 0

    def update(self):
        """Move the player"""
        keys = pygame.key.get_pressed()

        sprites = pygame.sprite.spritecollide(self, self.level.platforms, False)
        if not sprites:
            self.speed_y += 20
        else:
            self.in_fall = False
            if not self.in_fall and not self.in_air and self.rect.bottom >= sprites[0].rect.top:
                self.rect.bottom = sprites[0].rect.top + 20
            else:
                self.speed_y += 20

        # if the player hits the enemies he lose one live
        if pygame.sprite.spritecollide(self, self.level.enemies, False):
            self.lives -= 1
            # if the lives are less than one, game is over
            if self.lives < 1:
                running = False

        if keys[pygame.K_LEFT]:
            self.left_move()
        if keys[pygame.K_RIGHT]:
            self.right_move()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_UP] and self.current_animation not in (self.jump_r, self.jump_l):
            self.jump()

        if self.in_air and self.in_air_secs > 0:
            self.rect.y -= 30
            self.in_air_secs -= 1
            self.in_air = False if self.in_air_secs == 0 else self.in_air

        self.update_animation(keys)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.in_fall = True if self.speed_y > 0 else False

        self.speed_x = 0
        self.speed_y = 0

    def update_animation(self, keys):

        # changing direction of player
        if keys[pygame.K_LEFT]:
            self.player_facing = 'l'
        elif keys[pygame.K_RIGHT]:
            self.player_facing = 'r'

        # changing animation depending on pressed keys
        if self.in_fall or self.in_air:
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
        except ValueError:
            self.image = self.current_animation[0]

    def left_move(self):
        self.speed_x -= 20

    def right_move(self):
        self.speed_x += 20

    def jump(self):
        self.in_air = True
        self.in_air_secs = 25

    def shoot(self):
        pass
