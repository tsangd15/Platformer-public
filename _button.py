"""Button Module"""
import pygame
from _text import Text
from _settings import BLACK


class Button(pygame.sprite.Sprite):
    """Class for instantiating individual button sprites"""
    def __init__(self, width, height, text, textsize, idlecolor, hovercolor,
                 clickcolor, startx, starty, alpha=None):
        super().__init__()
        self.width = width
        self.height = height
        self.text = text
        self.textsize = textsize
        self.color_idle = idlecolor
        self.color_hover = hovercolor
        self.color_click = clickcolor

        self.alpha = alpha

        # set start pos and save spawn pos
        self.startx = startx
        self.starty = starty

        self.state_idle()

    def update_sprite(self, colors):
        """Method to update the button sprite's colours. 2 surfaces are
        created so that the opacity on the text and background is preserved.

        The parameter colors can be passed as a list or tuple in the form:
        (color of text, color of background) where the color is in the form of
        an RGB tuple.

        Alphas have been used to allow the background to have transparency.
        Alpha values range from 0 (fully transparent) to 255 (fully opaque)."""
        textcolor, bgcolor = colors

        # ---------- INSTANTIATE SURFACES AND MODIFY MAIN SURFACE ---------- #
        # instantiate main and background surface
        self.image = pygame.Surface([self.width, self.height])
        self.background = pygame.Surface([self.width, self.height])

        # remove default black color fill after surface instantiation from
        # main surface so that it's completely transparent
        self.image.set_colorkey(BLACK)

        # change main surface pixel format with per pixel alphas
        self.image = self.image.convert_alpha()

        # define rect instance for image
        self.rect = self.image.get_rect()

        # ---------- ADD BACKGROUND ---------- #
        if self.alpha is not None:
            # set opacity on background surface using given alpha value
            self.background.set_alpha(self.alpha)

        # fill background surface with background color
        self.background.fill(bgcolor)

        # render background surface onto main surface
        # background surface operated on with convert_alpha() function to
        # retain per pixel alphas
        self.image.blit(self.background.convert_alpha(), (0, 0))

        # ---------- ADD TEXT ---------- #
        # create text instance
        button_text = Text(self.text, self.textsize, "middle_center",
                           textcolor, None, self.rect.centerx,
                           self.rect.centery)
        # render text instance surface onto button surface
        self.image.blit(button_text.image, button_text.rect)

        # ---------- SET LOCATION ---------- #
        # set location on screen
        self.rect.x = self.startx
        self.rect.y = self.starty

    def state_idle(self):
        """Method to change the sprite image when idle (not hovered over)."""
        self.update_sprite(self.color_idle)

    def state_hover(self):
        """Method to change the sprite image when being hovered."""
        self.update_sprite(self.color_hover)

    def state_click(self):
        """Method to change the sprite image when being hovered."""
        self.update_sprite(self.color_click)
