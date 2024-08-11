"""Game Level - Pause Module"""
import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLUE
from _text import Text


class LevelPause():
    """Class for level pause screen"""
    def __init__(self):
        self.screens = ("resume", "quit")
        self.next_screen_index = -1

        self.sprites = pygame.sprite.Group()

        self.add_text()

        self.pause_begin = pygame.time.get_ticks()

        self.pause_end = None

        # calculate time paused
        self.duration = None

        self.duration = None

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_paused = Text("Game Paused", 60, "middle_center", BLUE, None,
                           WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        text_resume = Text("Press ESC to resume game.", 28, "middle_center",
                           BLUE, None, WINDOW_WIDTH/2, WINDOW_HEIGHT/2+40)
        self.sprites.add(text_paused, text_resume)

    def handle_events(self):
        """Get and handle events in the pygame event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_screen_index = 1  # self.screens[1] = "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_screen_index = 0  # self.screens[0] = "resume"

    def next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed."""
        if self.next_screen_index != -1:
            # if "resume" is selected:
            if self.next_screen_index == 0:
                # calculate the total time paused and save
                self.pause_end = pygame.time.get_ticks()
                self.duration = self.pause_end - self.pause_begin
            # return next screen's name
            return self.screens[self.next_screen_index]
        return None

    def update(self):
        """Handle events and return next screen to display."""
        self.handle_events()

        return self.next_screen()
