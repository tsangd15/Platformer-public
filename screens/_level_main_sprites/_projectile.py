"""Projectile Class Module"""
import pygame
from utils._settings import BLACK


class Projectile(pygame.sprite.Sprite):
    """Class for projectiles"""
    def __init__(self, color, startx, starty, velocity_x, velocity_y, damage,
                 width=9, height=9):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color

        # draw the square
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.rect.centerx = startx
        self.rect.centery = starty
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        # specify how much damage it inflicts on entities
        self.damage = damage
