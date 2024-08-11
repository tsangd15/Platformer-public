"""Root Menu Module"""
import pygame
from _button import Button
from _text import Text
from _functions import (set_button_idle, set_button_hover, set_button_click,
                        is_point_within_rect, return_button)
from _settings import WINDOW_WIDTH, RED, BLACK, CYAN, YELLOW


class RootMenu():
    """Class for handling root (or main) menu's sprites and logic."""
    def __init__(self, items):
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

        # store if cursor moved since last iteration
        self.cursor_moved = False

        # store when the highlighted item was last updated
        self.last_highlighted = pygame.time.get_ticks()
        self.highlightcooldown = 150

        # keep track if user has selected item in menu
        self.item_selected = False

        # store each menu item
        # in form ("PLAY", "LEADERBOARD")...
        self.items = items

        # store currently highlighted item using its index
        self.highlighted_item = 0

        self.add_title()

        self.add_buttons()

        self.update_cursor()

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
                self.terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # up arrow
                    self.arrow_up_pressed = True
                if event.key == pygame.K_DOWN:  # down arrow
                    self.arrow_down_pressed = True
                if (event.key == pygame.K_SPACE or  # spacebar
                    event.key == pygame.K_KP_ENTER or  # keypad enter
                   event.key == pygame.K_RETURN):  # main enter key
                    self.item_selected = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.arrow_up_pressed = False
                if event.key == pygame.K_DOWN:
                    self.arrow_down_pressed = False

            if event.type == pygame.MOUSEMOTION:
                self.cursor_moved = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    # get the button instance that is highlighted
                    highlightedbutton = return_button(self.items
                                                      [self.highlighted_item],
                                                      self.buttons)

                    # if button returned, check cursor is on the button
                    if highlightedbutton is not None:
                        if is_point_within_rect(event.pos, highlightedbutton):
                            # let menu know to call associated method
                            self.item_selected = True

                if event.button == 2:  # middle click
                    pass
                if event.button == 3:  # right click
                    pass
                if event.button == 4:  # scroll up
                    pass
                if event.button == 5:  # scroll down
                    pass

            # MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION.

    def is_button_hover(self):
        """Check if cursor is hovering over a button."""
        for button in self.buttons:
            if is_point_within_rect(self.cursor, button):
                self.set_highlighted_idle()
                self.highlighted_item = self.items.index(button.text)
                self.set_highlighted_hover()

    def terminate(self):
        """Simulate a quit item selection to tell the wider scope to terminate
        the program."""
        # set highlighted_item to point to index of "QUIT"
        self.highlighted_item = 4
        # simulate an item select event, causing "QUIT" to be returned to
        # wider scope
        self.item_selected = True

    def is_item_selected(self):
        """Check if a menu item has been selected by the user. If so, tell
        upper scope to suspend root menu iterations."""
        if self.item_selected:
            self.set_highlighted_click()
            return self.items[self.highlighted_item]

        # if no return function called, None is returned anyway but this line
        # makes it easier to comprehend
        return None

    def reset_item_selected(self):
        """Resets the item_selected attribute if it was previously True (i.e.
        different menu was just run because of last iteration, root menu is
        active again)."""
        if self.item_selected:
            self.item_selected = False
            self.set_highlighted_hover()

    def update_cursor(self):
        """Updates the cursor's stored location"""
        # store current cursor location
        self.cursor = pygame.mouse.get_pos()

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

        if self.cursor_moved:
            self.cursor_moved = False
            self.is_button_hover()

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""
        self.reset_item_selected()

        self.update_cursor()

        self.handle_events()

        self.update_highlighted()

        return self.is_item_selected()
