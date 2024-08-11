"""Save Score Screen Module"""
import pygame
from _screen import Screen
from _leaderboard_handler import ScoreHandler
from _text import Text
from _platform import Platform
from _functions import return_button, is_point_within_rect
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLUE, RED


class SaveScore(Screen):
    """Class to save score to scores.json"""
    def __init__(self, screens):
        super().__init__(screens)

        # add screen specific event handlers to list of event handlers
        self.event_handlers.extend((self.handle_events_keyboard,
                                   self.handle_events_mouse))

        # add the text and button sprites
        self.add_text()

        # hold if backspace is held down
        self.backspace = False

        # textbox contents
        self._text = ""

        # create and add text and textbox sprites
        self.add_textbox()

    @property
    def text(self):
        """Property decorator getter for text attribute"""
        return self._text

    @text.setter
    def text(self, new_text):
        """Property decorator setter for text attribute"""
        print("old:", self.text)
        print("newtext:", new_text)
        if len(new_text) <= 3:
            self._text = new_text

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_main = Text("Save Score", (400, 200), "top_center", BLUE, None,
                         WINDOW_WIDTH/2, 20)
        text_instruction = Text("Enter Player Tag:", 25, "top_center", BLUE,
                                None, WINDOW_WIDTH/2, 150)
        self.sprites.add(text_main, text_instruction)

    def add_textbox(self):
        """Instantiate and add the textbox and text sprites to the sprite
        group to be blitted to the screen."""
        # textbox sprite
        self.text_box = Platform(RED, 144 + 10, 45 + 10, 0, 0)
        # center the box to the center of the screen dimensions
        self.text_box.rect.centerx = WINDOW_WIDTH / 2
        self.text_box.rect.centery = WINDOW_HEIGHT / 2
        self.sprites.add(self.text_box)

        # text sprite
        self.text_sprite = Text(self.text, 50, "middle_center", BLUE, None,
                                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.sprites.add(self.text_sprite)

    def handle_events_keyboard(self, event):
        """Handle keyboard related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        # altf4 or window close button invokes pygame.QUIT
        if event.type == pygame.QUIT:
            self.terminate()

        elif event.type == pygame.TEXTINPUT:
            self.text += event.text

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # up arrow
                self.select_up = True
            elif event.key == pygame.K_DOWN:  # down arrow
                self.select_down = True
            elif (event.key == pygame.K_SPACE or  # spacebar
                  event.key == pygame.K_KP_ENTER or  # keypad enter
                  event.key == pygame.K_RETURN):  # main enter key
                self.confirmed = True
            elif event.key == pygame.K_BACKSPACE:
                self.backspace = True
            elif event.key == pygame.K_ESCAPE:  # escape key
                self.selected = "resume"
                self.confirmed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.select_up = False
            elif event.key == pygame.K_DOWN:
                self.select_down = False
            elif event.key == pygame.K_BACKSPACE:
                self.backspace = False

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

    def update_text(self):
        """Carry out all text update methods."""
        self.update_text_backspace()
        self.update_text_sprite()

    def update_text_sprite(self):
        """Update the text sprite's surface with new text string."""
        self.text_sprite.text = self.text
        self.text_sprite.update()

    def update_text_backspace(self):
        """Remove the last character on the text attribute if the backspace is
        being pressed."""
        if self.backspace:
            # remove last chracter from text string
            self.text = self.text[:-1]

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""

        # removed update_cursor and update_selected calls as no menu for
        # screen yet
        self.handle_events()

        self.update_text()

        return self.process_next_screen()
