"""Screen Class Module"""
import pygame
from _functions import (is_point_within_rect, set_button_idle,
                        set_button_hover, set_button_click)


class Screen():
    """Screen class to inherit from"""
    # ignore redundant pylint messages
    # pylint: disable=pointless-string-statement, too-many-instance-attributes
    def __init__(self, screens, has_quit_button=True):
        # store list of valid next screens
        self.screens = screens

        # define if internal quit button present or not
        self.has_quit_button = has_quit_button

        # store currently selected screen choice
        if has_quit_button:
            self._selected = self.screens[0]
        else:
            # set selected to second button as there's no internal quit button
            self._selected = self.screens[1]

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
    def selected(self):
        """Property decorator getter for selected attribute"""
        return self._selected

    @selected.setter
    def selected(self, screen_name):
        """Property decorator setter for selected attribute"""
        if screen_name in self.screens:
            if not self.confirmed:
                self._selected = screen_name
            else:
                print("Item already confirmed, selected is locked.")
        else:
            raise Exception(f"Invalid screen name passed: {screen_name}")

    def update_cursor(self):
        """Updates the cursor's stored location"""
        # store current cursor location
        self.cursor = pygame.mouse.get_pos()

    def terminate(self):
        """Simulate a quit item selection to tell the wider scope to terminate
        the program."""
        # set selected to "quit"
        self.selected = "quit"
        self.confirmed = True

    def set_selected_idle(self):
        """Set the currently selected screen's button to idle state."""
        set_button_idle(self.buttons, self.selected)

    def set_selected_hover(self):
        """Set the currently selected screen's button to hover state."""
        set_button_hover(self.buttons, self.selected)

    def set_selected_click(self):
        """Set the currently selected screen's button to click state."""
        set_button_click(self.buttons, self.selected)

    def is_button_hover(self):
        """Check if cursor is hovering over a button."""
        for button in self.buttons:
            if is_point_within_rect(self.cursor, button):
                self.set_selected_idle()
                self.selected = button.identifier
                self.set_selected_hover()

    def move_select_up(self):
        """Change the currently selected button to button above.
        The modulo function is used to correct index if it goes out of range.
        If it goes below 0 (before the top item) it's set to the bottom item.
        """
        # set currently selected item's button to idle state
        self.set_selected_idle()

        # find the new selected item's index, correct the index with modulo (%)
        new_selected_index = ((self.screens.index(self.selected) - 1)
                              % len(self.screens))

        # ignore invisible quit button
        if (self.has_quit_button is False) and (new_selected_index == 0):
            new_selected_index = len(self.screens) - 1

        # set the new selected item and change its button to hover state
        self.selected = self.screens[new_selected_index]
        self.set_selected_hover()

    def move_select_down(self):
        """Change the currently selected button to button below.
        The modulo function is used to correct index if it goes out of range.
        If it goes above the length of self.screens (after the bottom item)
        it's set to the top item."""
        # set currently selected item's button to idle state
        self.set_selected_idle()

        # find the new selected item's index, correct the index with modulo (%)
        new_selected_index = ((self.screens.index(self.selected) + 1)
                              % len(self.screens))

        # ignore invisible quit button
        if (self.has_quit_button is False) and (new_selected_index == 0):
            new_selected_index = 1

        # set the new selected item and change its button to hover state
        self.selected = self.screens[new_selected_index]
        self.set_selected_hover()

    def update_selected(self):
        """Check if the arrow keys are being pressed or mouse has moved. If so,
        update the menu accordingly by changing self.selected and updating
        the button state."""
        now = pygame.time.get_ticks()

        # if last keyboard navigation event occurred at least the cooldown
        # time, allow another keyboard navigation up/down event
        if now - self.last_selected >= self.select_cooldown:

            # change selected button to button above
            if self.select_up:
                self.move_select_up()
                self.last_selected = now

            # change selected button to button below
            if self.select_down:
                self.move_select_down()
                self.last_selected = now

        # update selected button on mouse movement event
        if self.cursor_moved:
            self.cursor_moved = False
            self.is_button_hover()

    def process_next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed)."""
        if self.confirmed:
            self.confirmed = False
            self.set_selected_click()
            return self.selected
        return None

    def handle_events(self):
        """Get and handle events from the pygame event queue.
        Each event gets iterated through each event handler to carry out tasks
        if it matches a specific event."""
        for event in pygame.event.get():
            # iterate through each event handler method
            for event_handler in self.event_handlers:
                # call event handler method with event as argument
                # if event matched, match = True, otherwise match = False
                match = event_handler(event)
                if match:  # if match == True
                    break  # end for loop

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""
        self.update_cursor()

        self.handle_events()

        self.update_selected()

        return self.process_next_screen()

    '''
    # ---------- Example text and button methods: ---------- #

    def add_text(self):
        """Add text instances to sprite group to be blitted to screen."""
        text_title = Text("Game Paused", 60, "middle_center", BLUE, None,
                          WINDOW_WIDTH/2, 100)
        self.sprites.add(text_title)

    def add_buttons(self):
        """Instantiate and add each button to sprites and buttons
        sprite group.
        A for loop iterates through all the menu items listed in self.items
        and creates a Button instance for each which is then added to the
        sprites and buttons sprite groups."""
        # define button colours
        button_idlecolor = (BLACK, RED)
        button_hovercolor = (CYAN, RED)
        button_clickcolor = (CYAN, YELLOW)

        # each iteration height increments 55
        # zip function to handle parallel iterator variables: item_name, height
        for item_name, height in zip(self.screens,
                                     range(190, 190+55*len(self.screens)+1, 55)
                                     ):
            button = Button(350, 50, item_name, 30, "top_center",
                            button_idlecolor, button_hovercolor,
                            button_clickcolor, WINDOW_WIDTH/2, height)
            self.sprites.add(button)
            self.buttons.add(button)

        # set top button as highlighted
        self.set_selected_hover()


    # ---------- Example event handlers: ---------- #

    def handle_events_keyboard(self, event):
        """Handle keyboard related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        # altf4 or window close button invokes pygame.QUIT
        if event.type == pygame.QUIT:
            self.terminate()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # up arrow
                self.select_up = True
            elif event.key == pygame.K_DOWN:  # down arrow
                self.select_down = True
            elif (event.key == pygame.K_SPACE or  # spacebar
                  event.key == pygame.K_KP_ENTER or  # keypad enter
                  event.key == pygame.K_RETURN):  # main enter key
                self.confirmed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.select_up = False
            elif event.key == pygame.K_DOWN:
                self.select_down = False

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match

    def handle_events_mouse(self, event):
        """Handle mouse related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        if event.type == pygame.MOUSEMOTION:
            self.cursor_moved = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left click
                # get the button instance that is selected
                selected_button = return_button(self.selected,
                                                self.buttons)

                # if button returned, check cursor is on the button
                if selected_button is not None:
                    if is_point_within_rect(event.pos, selected_button):
                        # let menu know to call associated method
                        self.confirmed = True

            elif event.button == 2:  # middle click
                pass
            elif event.button == 3:  # right click
                pass
            elif event.button == 4:  # scroll up
                pass
            elif event.button == 5:  # scroll down
                pass

            # MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match
    '''
