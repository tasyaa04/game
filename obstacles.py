"""Module used to create obstacles and platforms"""

from images import get_images
import pygame


class Platform(pygame.sprite.Sprite):
    """Platform the user can jump on"""

    def __init__(self, image_name, format_name, *groups):
        """Platform constructor. Setting an image to the platform
        and adding Sprite in needed sprite groups"""

        super().__init__(*groups)

        # setting an image
        self.image = get_images(image_name, format_name)[0]
        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    """Moving Platform the user can jump on and move with a platform"""

    def __init__(self, image_name, format_name, *groups):
        """Moving Platform constructor. You can set speed movement,
        borders of moving, player that you need to move and level"""

        super().__init__(image_name, format_name, *groups)

        # borders of moving
        self.border_left = 0
        self.border_right = 0
        self.border_top = 0
        self.border_bottom = 0

        # setting the player staying on platform and level
        self.player = None
        self.level = None

        # x and y speed
        self.x_speed = 0
        self.y_speed = 0

    def set_speed(self, speed_of_x, speed_of_y):
        """Function sets speed of moving platform"""

        self.x_speed = speed_of_x
        self.y_speed = speed_of_y

    def set_borders(self, left, right, top, bottom):
        """Function sets borders of moving platform"""

        self.border_left = left
        self.border_right = right
        self.border_top = top
        self.border_bottom = bottom

    def update(self):
        """Move the moving platform and player if he's on moving platform"""

        # Moving the platform left or right
        self.rect.x += self.x_speed

        # Checking if the player on platform
        if pygame.sprite.collide_rect(self, self.player):
            # Move player with speed of platform
            print(self.player.rect.bottom, self.rect.top)
            if self.player.rect.bottom <= self.rect.top + 30:
                self.player.rect.x += self.x_speed
                self.player.rect.y += self.y_speed

        # Check the borders of moving and see if we need to change direction of moving platform
        if self.rect.bottom > self.border_bottom or self.rect.top < self.border_top:
            # changing y direction
            self.y_speed *= -1

        if self.rect.left < self.border_left or self.rect.right > self.border_right:
            # changing x direction
            self.x_speed *= -1
