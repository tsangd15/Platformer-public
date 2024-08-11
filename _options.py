"""Options Screen Module"""
import json
import pygame
from _screen import Screen
from _text import Text
from _button import Button
from _functions import is_point_within_rect, return_button
from _settings import (WINDOW_WIDTH, RED, GREEN, DARK_RED, DARK_GREEN, BLUE,
                       BLACK, CYAN, YELLOW)


class Options(Screen):
    """Class for options screen
    Imported config is {"music": True,
                        "sound_effects": True}"""
    def __init__(self, screens):
        super().__init__(screens)
        self.load_config()

        # add screen specific event handlers to list of event handlers
        self.event_handlers.extend((self.handle_events_keyboard,
                                   self.handle_events_mouse))

        # add the text sprites
        self.add_text()
        self.add_buttons()

    def load_config(self):
        """Load the saved settings from config.json"""
        with open("config.json", "r") as file:
            contents = file.read()

        self.config = json.loads(contents)

    def save_config(self):
        """Save the current settings to config.json"""
        with open("config.json", "w") as file:
            file.write(json.dumps(self.config, indent=4, sort_keys=True) + "\n"
                       )

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_main = Text("OPTIONS", 56, "top_center", BLUE, None,
                         WINDOW_WIDTH/2, 20)
        text_music = Text("Background Music", 32, "middle_right", BLUE, None,
                          WINDOW_WIDTH/2 + 180, 250)
        text_sfx = Text("Sound Effects", 32, "middle_right", BLUE, None,
                        WINDOW_WIDTH/2 + 180, 350)
        self.sprites.add(text_main, text_music, text_sfx)

    def add_buttons(self):
        """Instantiate and add each button to sprites and buttons
        sprite group.
        A for loop iterates through all the menu items listed in self.items
        and creates a Button instance for each which is then added to the
        sprites and buttons sprite groups."""
        # back button
        # define button colours
        button_idlecolor = (BLACK, RED)
        button_hovercolor = (CYAN, RED)
        button_clickcolor = (CYAN, YELLOW)

        button_back = Button(50, 50, "<", (40, 40), "top_left",
                             button_idlecolor, button_hovercolor,
                             button_clickcolor, 20, 20, identifier="back")
        self.sprites.add(button_back)
        self.buttons.add(button_back)

        # define button colours
        button_idlecolor = (BLACK, RED)
        button_hovercolor = (DARK_RED, RED)
        button_clickcolor = (RED, DARK_GREEN)

        # each iteration height increments 55
        # zip function to handle parallel iterator variables
        config_states = self.config.values()
        button_text = []
        for value in config_states:
            if value is True:
                button_text.append("ON")
            elif value is False:
                button_text.append("OFF")
            else:
                raise Exception("Invalid value in config.json")

        for text, height, identifier in zip(button_text,
                                            range(250,
                                                  250+100*len(button_text),
                                                  100),
                                            self.config.keys()):
            button = Button(80, 50, text, 30, "middle_left",
                            button_idlecolor, button_hovercolor,
                            button_clickcolor, WINDOW_WIDTH/2 + 200, height,
                            identifier="config_" + identifier)
            self.sprites.add(button)
            self.buttons.add(button)

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

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match
