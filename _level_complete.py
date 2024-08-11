"""Game Level - Complete Module"""
import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLUE
from _text import Text


class LevelComplete():
    """Class for level complete screen"""
    def __init__(self, screens):
        self.sprites = pygame.sprite.Group()
        self.screens = screens
        self.next_screen_index = -1

        self.add_text()

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_main = Text("Level Completed!", (WINDOW_WIDTH-60,
                         WINDOW_HEIGHT-60), "middle_center", BLUE, None,
                         WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.sprites.add(text_main)

    def handle_events(self):
        """Get and handle events in the pygame event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_screen_index = 0

    def next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed."""
        if self.next_screen_index != -1:
            return self.screens[self.next_screen_index]
        return None

    def update(self):
        """Handle events and return next screen to display."""
        self.handle_events()

        return self.next_screen()
