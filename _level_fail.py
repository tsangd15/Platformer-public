"""Game Level - Fail Module"""
import pygame
from _screen import Screen
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLUE
from _text import Text


class LevelFail(Screen):
    """Class for level fail screen"""
    def __init__(self, screens):
        super().__init__(screens)

        # add screen specific event handlers to list of event handlers
        self.event_handlers.extend((self.handle_events_keyboard,))

        # add the text sprites
        self.add_text()

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_main = Text("Level Failed!", (WINDOW_WIDTH-60,
                         WINDOW_HEIGHT-60), "middle_center", BLUE, None,
                         WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.sprites.add(text_main)

    def handle_events_keyboard(self, event):
        """Handle keyboard related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        # altf4 or window close button invokes pygame.QUIT
        if event.type == pygame.QUIT:
            self.terminate()

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match

    def update(self):
        """Update the menu by checking for any events and updating attributes
        and button states as needed."""

        # removed update_cursor and update_selected calls as no menu for
        # screen yet
        self.handle_events()

        return self.process_next_screen()
