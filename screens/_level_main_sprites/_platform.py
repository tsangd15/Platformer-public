"""Platform Class Module"""
import pygame
from utils._settings import BLACK


class Platform(pygame.sprite.Sprite):
    """Class for platforms"""
    def __init__(self, color, width, height, startx, starty):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color

        # draw rectangle
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = startx, starty

        # define sprite's mask for collision calculation between line and
        # platform for enemy vision
        self.mask = pygame.mask.from_surface(self.image)
