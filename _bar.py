"""Bar Module"""
import pygame
from _settings import BLACK


class Bar(pygame.sprite.Sprite):
    """Class for bars. Individual bar capacity is determined by percentage.
    0% being empty, 100% being full size"""
    def __init__(self, color, width, height, startx, starty):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color
        self.image.fill(self.color)

        self.width = width
        self.height = height

        self.maximum = 100
        self._capacity = self.maximum

        # draw the square
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

        self.rect = self.image.get_rect()

        self.startx, self.starty = startx, starty
        self.rect.x, self.rect.y = startx, starty

    @property
    def capacity(self):
        """Property decorator for capacity attribute"""
        return self._capacity

    @capacity.setter
    def capacity(self, new_capacity):
        if 0 <= new_capacity <= 100:
            self._capacity = new_capacity
        else:
            raise Exception("Invalid bar 'capacity'")

    def update(self):
        """Update the bar sprite's size based on current capacity"""
        # transform image scale with capacity percentage width
        self.image = pygame.transform.scale(self.image,
                                            [int((self.capacity/self.maximum) *
                                                 self.width),
                                             self.height])

        # update rect with new image
        pygame.draw.rect(self.image, self.color,
                         [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.startx, self.starty  # set location
