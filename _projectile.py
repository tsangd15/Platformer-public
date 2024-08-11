"""Projectile Class Module"""
import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK


class Projectile(pygame.sprite.Sprite):
    """Class for projectiles"""
    def __init__(self, color, startx, starty, velocity_x, velocity_y,
                 width=100, height=100):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color

        # draw the square
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.rect.x = startx
        self.rect.y = starty
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self):
        """Update velocity each frame"""
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # kill if off-screen
        if ((self.rect.left > WINDOW_WIDTH) or
           (self.rect.right < 0) or
           (self.rect.bottom < 0) or
           (self.rect.top > WINDOW_HEIGHT)):
            self.kill()
