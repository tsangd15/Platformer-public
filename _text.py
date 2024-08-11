"""Text Class Module"""
import pygame
import pygame.freetype


class Text(pygame.sprite.Sprite):
    """Class for creating text sprites in pygame significantly more easily and
    more organised. """
    def __init__(self, text, size, fgcolour, bgcolour, startx, starty):
        super().__init__()

        self.text = text
        self.fgcolour = fgcolour
        self.bgcolour = bgcolour
        self.size = size
        self.number = 0

        # font file/name, font size
        self.font = pygame.freetype.Font(None, self.size)

        # function returns text as rendered syrface and rect object instance
        # parameters: text, fgcolour, bgcolour
        self.image, self.rect = self.font.render(self.text, self.fgcolour,
                                                 self.bgcolour)

        # set location of text
        self.startx = startx
        self.starty = starty
        self.rect.x, self.rect.y = startx, starty

    def rect_info(self):
        """For debugging, outputs generated text sprite's rect details
        for help adjusting on text placement"""
        print("width,height:", self.rect.width, self.rect.height,
              "\ncenter:", self.rect.center,
              "\ntopleft:", self.rect.topleft)

    def changeimage(self):
        self.number += 1
        self.text = "Score: " + str(self.number)
        self.image, self.rect = self.font.render(self.text, self.fgcolour, self.bgcolour)
        self.rect.x, self.rect.y = self.startx, self.starty
