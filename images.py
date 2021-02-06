"""Module used to process the images"""

import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_images(file_name, format_name='.png'):
    images = []
    if '...' in file_name:  # for the objects needed an animation
        start, end = file_name.split('...')
        *name, start = start.split('_')
        start, end = map(int, [start, end])
        name = '_'.join(name)

        for i in range(start, end + 1):
            image_name = '_'.join((name, str(i).zfill(4))) + format_name
            images.append(load_image(image_name))
    else:
        images.append(load_image(file_name + format_name))

    return images
