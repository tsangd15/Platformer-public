import pygame
from _settings import BLACK


class Entity(pygame.sprite.Sprite):

    def __init__(self, color, width, height, startx, starty):
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
