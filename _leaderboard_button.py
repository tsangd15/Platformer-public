"""Leaderboard Local/Global Toggle Button Module"""
from _button import Button
from _settings import (BLACK, PURPLE, CYAN, WHITE, YELLOW, BLUE, ORANGE)


# local colour states
local_idle = (PURPLE, YELLOW)
local_hover = (CYAN, PURPLE)
local_click = (WHITE, BLACK)

# global colour states
global_idle = (BLUE, ORANGE)
global_hover = (ORANGE, BLUE)
global_click = (WHITE, BLACK)


class ToggleButton(Button):
    """Class for toggle buttons"""
    def __init__(self, width, height, toggle, textsize, alignment, startx,
                 starty, alpha=None, identifier=None):
        if toggle == "local":
            idlecolor = local_idle
            hovercolor = local_hover
            clickcolor = local_click
        elif toggle == "global":
            idlecolor = global_idle
            hovercolor = global_hover
            clickcolor = global_click
        else:
            raise Exception(f"Invalid toggle input: {toggle}")
        super().__init__(width, height, toggle, textsize, alignment, idlecolor,
                         hovercolor, clickcolor, startx, starty, alpha=alpha,
                         identifier=identifier)

    def toggle_local(self):
        """Change the button state colours to local theme."""
        self.color_idle = local_idle
        self.color_hover = local_hover
        self.color_click = local_click

        self.text = "local"

        self.state_hover()

    def toggle_global(self):
        """Change the button state colours to global theme."""
        self.color_idle = global_idle
        self.color_hover = global_hover
        self.color_click = global_click

        self.text = "global"

        self.state_hover()
