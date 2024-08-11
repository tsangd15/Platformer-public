"""Options On/Off Button Module"""
from _button import Button
from _settings import (BLACK, DARK_GREEN, DARK_RED, GREEN, RED, PURPLE, CYAN,
                       WHITE)


# on colour states
on_idle = (BLACK, DARK_GREEN)
on_hover = (PURPLE, GREEN)
on_click = (WHITE, BLACK)

# off colour states
off_idle = (BLACK, DARK_RED)
off_hover = (CYAN, RED)
off_click = (WHITE, BLACK)


class ToggleButton(Button):
    """Class for toggle buttons"""
    def __init__(self, width, height, toggle, textsize, alignment, startx,
                 starty, alpha=None, identifier=None):
        if toggle == "on":
            idlecolor = on_idle
            hovercolor = on_hover
            clickcolor = on_click
        elif toggle == "off":
            idlecolor = off_idle
            hovercolor = off_hover
            clickcolor = off_click
        else:
            raise Exception(f"Invalid toggle input: {toggle}")
        super().__init__(width, height, toggle, textsize, alignment, idlecolor,
                         hovercolor, clickcolor, startx, starty, alpha=alpha,
                         identifier=identifier)

    def toggle_on(self):
        """Change the button state colours to on theme and text to "ON"."""
        self.color_idle = on_idle
        self.color_hover = on_hover
        self.color_click = on_click

        self.text = "ON"

        self.state_hover()

    def toggle_off(self):
        """Change the button state colours to off theme and text to "OFF"."""
        self.color_idle = off_idle
        self.color_hover = off_hover
        self.color_click = off_click

        self.text = "OFF"

        self.state_hover()
