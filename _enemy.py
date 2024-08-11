"""Enemy Class Module"""
import pygame
from _entity import Entity
from _settings import BLACK


class Enemy(Entity):
    """Class for enemy"""
    def __init__(self, color, width, height, startx=430, starty=400):
        super().__init__(color, width, height, startx, starty)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color
        self.health = 50
        self.number = 0

        # draw the square
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.rect.x = startx
        self.rect.y = starty

    def hit(self):
        """Method to reduce health when hit by projectile."""
        self.health -= 5
        print("hit", self.number)
        self.number += 1

    def update(self):
        """Method to check if health is below 0, if so, despawn enemy."""
        if self.health <= 0:
            self.kill()
