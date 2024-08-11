"""Text Class Module"""
import pygame
import pygame.freetype


class Text(pygame.sprite.Sprite):
    """Class for creating text sprites in pygame significantly more easily and
    more organised. """
    def __init__(self, text, size, fgcolour, bgcolour, startx, starty):
        super().__init__()

        # store arguments
        self._text = text
        self.fgcolour = fgcolour
        self.bgcolour = bgcolour
        self._startx = startx
        self._starty = starty

        self.size = size
        self.number = 0

        # instantiate font object instance
        # parameters: font file/name, font size
        self.font = pygame.freetype.Font("PressStart2P-Regular.ttf", self.size)

        # set the sprite's image and rect
        self.update()

    def rect_info(self):
        """For debugging, outputs generated text sprite's rect details
        for help adjusting on text placement"""
        print("width,height:", self.rect.width, self.rect.height,
              "\ncenter:", self.rect.center,
              "\ntopleft:", self.rect.topleft)

    def changeimage(self):
        """For debugging, increments and updates the text sprite"""
        self.number += 1
        self.text = "Score: " + str(self.number)

    def update(self):
        """Update the sprite's image and rect"""
        # function returns text as rendered syrface and rect object instance
        # parameters: text, fgcolour, bgcolour
        self.image, self.rect = self.font.render(self.text, self.fgcolour,
                                                 self.bgcolour)
        self.rect.x, self.rect.y = self.startx, self.starty

    @property
    def text(self):
        """Property decorator for text attribute"""
        return self._text

    @text.setter
    def text(self, new_text):
        if isinstance(new_text, str):
            self._text = new_text
            self.update()
        else:
            raise Exception("new_text not string type")

    @property
    def startx(self):
        """Property decorator for startx attribute"""
        return self._startx

    @startx.setter
    def startx(self, new_startx):
        if isinstance(int(new_startx), int):
            self._startx = int(new_startx)
            self.update()
        else:
            raise Exception("new_startx not int type")

    @property
    def starty(self):
        """Property decorator for starty attribute"""
        return self._starty

    @starty.setter
    def starty(self, new_starty):
        if isinstance(int(new_starty), int):
            self._starty = int(new_starty)
            self.update()
        else:
            raise Exception("new_starty not int type")
