"""Leaderboard Screen Module"""
import pygame
from _screen import Screen
from _settings import WINDOW_WIDTH, BLACK, RED, CYAN, YELLOW
from _text import Text
from _button import Button
from _functions import is_point_within_rect, return_button


class Leaderboard(Screen):
    """Class for leaderboard screen"""
    def __init__(self, screens):
        super().__init__(screens)

        # add screen specific event handlers to list of event handlers
        self.event_handlers.extend((self.handle_events_keyboard,
                                   self.handle_events_mouse))

        # add the text and button sprites
        self.add_text()
        self.add_buttons()

    def add_text(self):
        """Add text instances to sprite group to be blitted to screen."""
        text_title = Text("LEADERBOARD", (600, 400), "top_center", RED, None,
                          WINDOW_WIDTH/2, 20)
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

        button_back = Button(50, 50, "<", (40, 40), "top_left",
                             button_idlecolor, button_hovercolor,
                             button_clickcolor, 20, 20, identifier="root_menu")
        self.sprites.add(button_back)
        self.buttons.add(button_back)

        # set top button as highlighted
        self.set_selected_hover()

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
