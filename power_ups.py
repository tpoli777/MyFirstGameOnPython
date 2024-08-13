import random

import pygame

from constants import BLACK, HEIGHT
from textures import powerup_images


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['health', 'gun', 'shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self, group_dict):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()
