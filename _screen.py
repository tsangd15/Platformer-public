"""Screen Class Module"""
import pygame
from _functions import (is_point_within_rect, set_button_idle,
                        set_button_hover, set_button_click)


class Screen():
    """Screen class to inherit from"""
    # ignore redundant pylint messages
    # pylint: disable=pointless-string-statement, too-many-instance-attributes
    def __init__(self, screens):
        # store list of valid next screens
        self.screens = screens

        # store currently selected screen choice
        self._next_screen = None

        # define sprite groups
        self.sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        # store if selected button should move up/down
        # e.g. up arrow pressed, button above current selected button becomes
        # the new selected button
        self.select_up = False
        self.select_down = False

        # store if cursor has moved since last iteration
        self.cursor_moved = False

        # store when the selected choice was last updated
        self.last_selected = pygame.time.get_ticks()
        self.select_cooldown = 150

        # keep track if user has confirmed choice (e.g. clicked/press enter)
        self.confirmed = False

        # update the stored cursor location
        self.update_cursor()

        # list of event handler sub-functions
        self.event_handlers = []

    @property
    def next_screen(self):
        """Property decorator getter for next_screen attribute"""
        return self._next_screen

    @next_screen.setter
    def next_screen(self, screen_name):
        """Property decorator setter for next_screen attribute"""
        if screen_name in self.screens:
            self._next_screen = screen_name
        else:
            raise Exception(f"Invalid screen name passed: {screen_name}")

    def update_cursor(self):
        """Updates the cursor's stored location"""
        # store current cursor location
        self.cursor = pygame.mouse.get_pos()

    def terminate(self):
        """Simulate a quit item selection to tell the wider scope to terminate
        the program."""
        # set next_screen to "quit"
        self.next_screen = "quit"
        self.confirmed = True

    def set_selected_idle(self):
        """Set the currently selected screen's button to idle state."""
        set_button_idle(self.buttons, self.next_screen)

    def set_selected_hover(self):
        """Set the currently selected screen's button to hover state."""
        set_button_hover(self.buttons, self.next_screen)

    def set_selected_click(self):
        """Set the currently selected screen's button to click state."""
        set_button_click(self.buttons, self.next_screen)

    def is_button_hover(self):
        """Check if cursor is hovering over a button."""
        for button in self.buttons:
            if is_point_within_rect(self.cursor, button):
                self.set_selected_idle()
                self.next_screen = button.text
                self.set_selected_hover()

    def move_select_up(self):
        """Change the currently selected button to button above."""
        self.set_selected_idle()
        new_selected_index = (self.screens.index(self.next_screen) - 1) % 5
        self.next_screen = self.screens[new_selected_index]
        self.set_selected_hover()

    def move_select_down(self):
        """Change the currently selected button to button below."""
        self.set_selected_idle()
        new_selected_index = (self.screens.index(self.next_screen) + 1) % 5
        self.next_screen = self.screens[new_selected_index]
        self.set_selected_hover()

    def update_selected(self):
        """Check if the arrow keys are being pressed. If so, update the menu
        accordingly by changing self.next_screen and updating the button
        state.

        The modulo function is used to correct the index point attribute
        self.highlighted_item if it goes out of range.
        If it goes below 0 (before the top item) the pointer is set to the
        bottom item.
        If it goes above 4 (after the bottom item) the pointer is set to the
        top item."""
        now = pygame.time.get_ticks()

        if now - self.last_selected >= self.select_cooldown:

            if self.select_up:
                self.move_select_up()
                self.last_selected = now

            if self.select_down:
                self.move_select_down()
                self.last_selected = now

        if self.cursor_moved:
            self.cursor_moved = False
            self.is_button_hover()

    def process_next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed)."""
        if self.confirmed:
            self.confirmed = False
            self.set_selected_click()
            return self.next_screen
        return None

    def handle_events(self):
        """Get and handle events from the pygame event queue."""
        for event in pygame.event.get():
            # iterate through each event handler method
            for event_handler in self.event_handlers:
                # call event handler method with event as argument
                event_handler(event)

    '''
    Sample event handlers:

    def handle_events_keyboard(self, event):
        if event.type == pygame.QUIT:
            self.terminate()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # up arrow
                self.select_up = True
            if event.key == pygame.K_DOWN:  # down arrow
                self.select_down = True
            if (event.key == pygame.K_SPACE or  # spacebar
                event.key == pygame.K_KP_ENTER or  # keypad enter
               event.key == pygame.K_RETURN):  # main enter key
                self.confirmed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.select_up = False
            if event.key == pygame.K_DOWN:
                self.select_down = False

    def handle_events_mouse(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.cursor_moved = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                # get the button instance that is selected
                selected_button = return_button(self.next_screen,
                                                self.buttons)

                # if button returned, check cursor is on the button
                if selected_button is not None:
                    if is_point_within_rect(event.pos, selected_button):
                        # let menu know to call associated method
                        self.confirmed = True

            if event.button == 2:  # middle click
                pass
            if event.button == 3:  # right click
                pass
            if event.button == 4:  # scroll up
                pass
            if event.button == 5:  # scroll down
                pass

            # MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION
    '''

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""
        self.update_cursor()

        self.handle_events()

        self.update_selected()

        return self.process_next_screen()
