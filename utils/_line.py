"""Line Sprite Module"""
import pygame
from ._settings import BLACK, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT


class Line(pygame.sprite.Sprite):
    """Class for line sprite"""
    def __init__(self, point1, point2):
        super().__init__()
        # create sprite image and rect
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # draw initial line
        self.update_location(point1, point2)

    def update_location(self, point1, point2):
        """Fill image surface and draw line with given points."""
        # clear image of previous line
        self.image.fill(BLACK)
        # draw new line with given points onto image
        # 5th argument (integer) is line thickness
        pygame.draw.line(self.image, WHITE, point1, point2, 9)

        # define sprite's mask for collision calculation
        self.mask = pygame.mask.from_surface(self.image)
