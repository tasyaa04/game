"""Module used to interact with player"""

import pygame
import os
from images import get_images
from random import randint
from levels import HEIGHT


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

        self.jump_sound = pygame.mixer.Sound('sfx/sfx_player_jump_01.wav')
        self.jump_sound.set_volume(0.1)
        self.shoot_sound = pygame.mixer.Sound('sfx/sfx_player_default_fire_loop_01.wav')
        self.shoot_sound.set_volume(0.2)
        self.shoot_sound_playing = False

        # current list of images
        self.current_animation = self.idle_r

        self.image = self.current_animation[0]
        self.rect = self.image.get_rect()

        self.running = True

        # speed of player
        self.speed_x = 0
        self.speed_y = 0

        self.level = None
        self.lives = 3

        # used to manage interacting with the platforms
        self.in_air = False
        self.in_fall = True
        self.in_air_secs = 0

        self.clock = pygame.time.Clock()
        self.time = 0

        self.bullets = pygame.sprite.Group()

    def update(self):
        """Move the player"""
        keys = pygame.key.get_pressed()

        sprites = pygame.sprite.spritecollide(self, self.level.platforms, False)
        if not sprites:
            self.speed_y += 20
        else:
            self.in_fall = False
            if not self.in_fall and not self.in_air and self.rect.bottom <= sprites[0].rect.top + 50:
                self.rect.bottom = sprites[0].rect.top + 20
            else:
                self.in_fall = True
                self.speed_y += 20

        # if the player hits the enemies he lose one live
        if pygame.sprite.spritecollide(self, self.level.enemies, False):
            self.lives -= 1
            # if the lives are less than one, game is over
            if self.lives < 1:
                self.running = False

        if self.rect.bottom > HEIGHT:
            self.running = False

        if keys[pygame.K_LEFT]:
            self.left_move()
        if keys[pygame.K_RIGHT]:
            self.right_move()
        if keys[pygame.K_SPACE]:
            self.shoot()
            if not self.shoot_sound_playing:
                self.shoot_sound.play(-1, maxtime=0)
                self.shoot_sound_playing = True
        else:
            self.shoot_sound.stop()
            self.shoot_sound_playing = False
        if keys[pygame.K_UP] and self.current_animation not in (self.jump_r, self.jump_l):
            self.jump_sound.play(0)
            self.jump()

        if self.in_air and self.in_air_secs > 0:
            self.rect.y -= 60
            self.in_air_secs -= 1
            self.in_air = False if self.in_air_secs == 0 else self.in_air

        self.update_animation(keys)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.in_fall = True if self.speed_y > 0 else False

        self.speed_x = 0
        self.speed_y = 0

        self.time += self.clock.tick()
        self.bullets.update()

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
            if self.current_animation in (self.idle_l, self.idle_r):
                self.image = self.current_animation[(self.time // 90) % len(self.current_animation)]
            else:
                self.image = self.current_animation[(self.time // 60) % len(self.current_animation)]
        except ValueError:
            self.image = self.current_animation[0]

    def left_move(self):
        self.speed_x -= 20

    def right_move(self):
        self.speed_x += 20

    def jump(self):
        self.in_air = True
        self.in_air_secs = 6

    def shoot(self):
        try:
            last_bullet = self.bullets.sprites()[-1]
            if ((last_bullet.rect.x > self.rect.x + 400) and (last_bullet.facing == 'r')) or \
                    ((last_bullet.rect.x < self.rect.x - 400) and (last_bullet.facing == 'l')):
                Bullet(self, self.bullets)
        except IndexError:
            Bullet(self, self.bullets)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, *groups):
        super().__init__(*groups)

        self.clock = pygame.time.Clock()
        self.time = 0

        self.groups = groups
        self.facing = player.player_facing
        self.r_animation = get_images(f'bullet{os.sep}bullet_0001...0008')
        self.l_animation = [pygame.transform.flip(x, True, False) for x in self.r_animation]
        self.current_animation = self.r_animation if self.facing == 'r' else self.l_animation
        self.image = self.current_animation[0]
        self.rect = self.image.get_rect()
        self.rect.y = randint(player.rect.y, player.rect.y + 100)
        self.rect.x = player.rect.x + 75 if self.facing == 'r' else player.rect.left - 75
        self.rect.width = 150
        self.rect.height = 50

    def update(self):
        if self.facing == 'l':
            self.rect.x -= 50
        elif self.facing == 'r':
            self.rect.x += 50

        self.image = self.current_animation[(self.time // 75) % len(self.current_animation)]

        self.time += self.clock.tick()
        if self.rect.x not in range(0, 1920):
            for group in self.groups:
                group.remove(self)
            del self
