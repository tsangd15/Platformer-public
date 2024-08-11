"""Root Menu Module"""
import pygame
from _button import Button
from _text import Text
from _functions import set_button_idle, set_button_hover, set_button_click
from _settings import WINDOW_WIDTH, RED, BLACK, CYAN, YELLOW


class RootMenu():
    """Class for handling root (or main) menu's sprites and logic."""
    def __init__(self, items):
        # tell wider scope to terminate program
        self.terminate = False

        # define sprite groups
        # sprites contains all sprites (global sprite group)
        self.sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        # define button colours
        self.button_idlecolor = (BLACK, RED)
        self.button_hovercolor = (CYAN, RED)
        self.button_clickcolor = (CYAN, YELLOW)

        # store if up/down arrow keys are pressed
        self.arrow_up_pressed = False
        self.arrow_down_pressed = False

        # store when the highlighted item was last updated
        self.last_highlighted = pygame.time.get_ticks()
        self.highlightcooldown = 150

        # store each menu item
        self.items = items

        # store currently highlighted item using its index
        self.highlighted_item = 0

        self.add_title()

        self.add_buttons()

    def add_title(self):
        """Instantiate and add title text to sprites sprite group."""
        text_title = Text("PLATFORMER", (600, 400), "top_center", RED, None,
                          WINDOW_WIDTH/2, 20)
        self.sprites.add(text_title)

    def add_buttons(self):
        """Instantiate and add each button to sprites and buttons
        sprite group.

        A for loop iterates through all the menu items listed in self.items
        and creates a Button instance for each which is then added to the
        sprites and buttons sprite groups."""
        # each iteration height increments 55
        # zip function to handle parallel iterator variables: item_name, height
        for item_name, height in zip(self.items,
                                     range(190, 190+55*len(self.items)+1, 55)):
            button = Button(350, 50, item_name, 30, "top_center",
                            self.button_idlecolor, self.button_hovercolor,
                            self.button_clickcolor, WINDOW_WIDTH/2, height)
            self.sprites.add(button)
            self.buttons.add(button)

        # set top button as highlighted
        self.set_highlighted_hover()

    def set_highlighted_idle(self):
        """Set the currently highlighted item's button to idle state."""
        set_button_idle(self.buttons, self.items[self.highlighted_item])

    def set_highlighted_hover(self):
        """Set the currently highlighted item's button to hover state."""
        set_button_hover(self.buttons, self.items[self.highlighted_item])

    def set_highlighted_click(self):
        """Set the currently highlighted item's button to click state."""
        set_button_click(self.buttons, self.items[self.highlighted_item])

    def handle_events(self):
        """Get and handle events from pygame event queue."""
        # keybind detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # up arrow
                    self.arrow_up_pressed = True
                if event.key == pygame.K_DOWN:  # down arrow
                    self.arrow_down_pressed = True
                if (event.key == pygame.K_SPACE or  # spacebar
                    event.key == pygame.K_KP_ENTER or  # keypad enter
                   event.key == pygame.K_RETURN):  # main enter key
                    pass

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.arrow_up_pressed = False
                if event.key == pygame.K_DOWN:
                    self.arrow_down_pressed = False

            # if event.type == pygame.
            # MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION.

            # self.update_mouse()

    def update_highlighted(self):
        """Check if the arrow keys are being pressed. If so, update the menu
        accordingly by changing self.highlighted_item and updating the button
        state.

        The modulo function is used to correct the index point attribute
        self.highlighted_item if it goes out of range.
        If it goes below 0 (before the top item) the pointer is set to the
        bottom item.
        If it goes above 4 (after the bottom item) the pointer is set to the
        top item."""

        now = pygame.time.get_ticks()

        if now - self.last_highlighted >= self.highlightcooldown:

            if self.arrow_up_pressed:
                # decrement highlighted item index
                self.set_highlighted_idle()
                self.highlighted_item = (self.highlighted_item - 1) % 5
                self.set_highlighted_hover()
                self.last_highlighted = now

            if self.arrow_down_pressed:
                # increment highlighted item index
                self.set_highlighted_idle()
                self.highlighted_item = (self.highlighted_item + 1) % 5
                self.set_highlighted_hover()
                self.last_highlighted = now

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""

        self.handle_events()

        self.update_highlighted()
