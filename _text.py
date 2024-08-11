"""Text Class Module"""
import pygame
import pygame.freetype
from _functions import check_alignment, align


class Text(pygame.sprite.Sprite):
    """Class for creating text sprites in pygame significantly more easily and
    more organised. """
    def __init__(self, text, size, alignment, fgcolour, bgcolour, startx,
                 starty):
        super().__init__()

        # ----- store arguments ----- #
        self._text = text
        self.fgcolour = fgcolour
        self.bgcolour = bgcolour
        self._startx = startx
        self._starty = starty
        self.font_size = 20

        # ----- instantiate font object instance ----- #
        self.update_font()

        # ----- configure text sprite alignment ----- #
        self.alignment = check_alignment(alignment)

        # ----- configure text sprite font size ----- #
        # specific font size given
        if isinstance(size, int):
            self.font_size = size
        # specific desired rect dimensions given
        elif isinstance(size, tuple):
            # find maximum font size that fits these dimensions
            self.autofit(size)

        self.number = 0

        # set the sprite's image and rect
        self.update()

    def autofit(self, desired_dimensions):
        """Procedure that finds and sets the maximum font size that can fit
        inside the given dimensions.

        A while loop is used to iterate through different font sizes.
        If font size too big, font size decreased with the upper variable
        telling the procedure that the font was previously too big;
        otherwise font size increased.

        If font size not too big and upper variable is true, we know the
        current font in self.font_size is the maximum integer font size."""
        dimensions_x, dimensions_y = desired_dimensions
        fitting = True
        upper = False

        # while loop to find biggest font that fits in dimensions
        while fitting:
            # update font sprite with new font size
            self.update()

            # check if sprite bigger than desired dimensions
            if ((self.rect.width > dimensions_x) or
               (self.rect.height > dimensions_y)):
                # decrease font size
                self.font_size -= 1
                # tell function we were too big
                upper = True

            # sprite is within desired dimensions
            else:
                # if previously too big
                if upper:
                    # this is the maximum font size that fits, so end loop
                    fitting = False
                # otherwise too small, increase font size
                else:
                    self.font_size += 1

    def update_font(self):
        """Update the Font object with new font size."""
        # parameters: font file/name, font size
        self.font = pygame.freetype.Font("PressStart2P-Regular.ttf",
                                         self.font_size)

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
        """Update the sprite's font, image and rect"""
        # function returns text as rendered syrface and rect object instance
        # parameters: text, fgcolour, bgcolour
        self.update_font()
        self.image, self.rect = self.font.render(self.text, self.fgcolour,
                                                 self.bgcolour)
        align(self.alignment, self.rect, self.startx, self.starty)

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
