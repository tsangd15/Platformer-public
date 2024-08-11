"""Button Module"""
import pygame


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
        textcolor, bgcolor = colors
        self.image = pygame.Surface([self.width, self.height])

        if self.alpha is not None:
            self.image.set_alpha(self.alpha)

        self.image.fill(bgcolor)

        # draw the square
        pygame.draw.rect(self.image, bgcolor, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

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
