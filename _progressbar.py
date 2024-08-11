"""Progress Bar Module"""
import pygame
from _bar import Bar


class ProgressBar():
    """Class for progress bars"""
    def __init__(self, width, height, fgcolour, bgcolour, startx, starty,
                 maximum):
        # create individual bars and add to sprite group
        self.outline = 2
        self.bars = pygame.sprite.Group()
        self.bar_bg = Bar(bgcolour, width, height, startx, starty)
        self.bar_fg = Bar(fgcolour, width-(2*self.outline),
                          height-(2*self.outline), startx+(self.outline),
                          starty+(self.outline))
        self.bars.add(self.bar_bg, self.bar_fg)

        self.maximum = maximum
        self._value = maximum

    @property
    def value(self):
        """Property decorator for value attribute"""
        return self._value

    @value.setter
    def value(self, new_value):
        """Property decorator setter for value attribute"""
        if 0 <= new_value <= self.maximum:
            self._value = new_value
            self.update()
        elif new_value < 0:
            self._value = 0
            self.update()

    def update(self):
        """Update progress bar with new capacity

        This method sets a new capacity for the bar as a percentage (out of
        the maximum, self.maximum). The bar's update() method is then called to
        create the new image and rect for the new capacity."""
        self.bar_fg.capacity = (self.value/self.maximum)*100
        self.bar_fg.update()
