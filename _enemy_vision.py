"""Enemy Vision Module"""
import pygame
from _settings import BLACK, PINK


class EnemyVision(pygame.sprite.Sprite):
    """Class for enemy sight circle."""
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.set_colorkey(BLACK)
        self.image.set_alpha(150)

        # draw circle onto image with centre at centre of image
        pygame.draw.circle(self.image, PINK, (radius, radius), radius)
        self.rect = self.image.get_rect()

    def update_location(self, centerx, centery):
        """Update the vision sprite's location with a centre coordinate."""
        self.rect.centerx = centerx
        self.rect.centery = centery
