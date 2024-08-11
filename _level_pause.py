"""Game Level - Pause Module"""
import pygame
from _settings import (WINDOW_WIDTH, BLUE, BLACK, RED, CYAN, YELLOW)
from _text import Text
from _button import Button


class LevelPause():
    """Class for level pause screen"""
    def __init__(self, screens):
        self.screens = screens
        self._next_screen = None

        self.sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.add_text()

        self.add_buttons()

        self.pause_begin = pygame.time.get_ticks()

        self.pause_end = None

        # calculate time paused
        self.duration = None

        self.duration = None

    def add_text(self):
        """Add text to sprite group to be blitted to screen."""
        text_title = Text("Game Paused", 60, "middle_center", BLUE, None,
                          WINDOW_WIDTH/2, 100)
        self.sprites.add(text_title)

    def add_buttons(self):
        """Add menu buttons to sprite group to be blitted to screen."""
        # define button colours
        button_idlecolor = (BLACK, RED)
        button_hovercolor = (CYAN, RED)
        button_clickcolor = (CYAN, YELLOW)

        for item_name, height in zip(self.screens,
                                     range(190, 190+55*len(self.screens)+1, 55)
                                     ):
            button = Button(350, 50, item_name.upper(), 30, "top_center",
                            button_idlecolor, button_hovercolor,
                            button_clickcolor, WINDOW_WIDTH/2, height)
            self.sprites.add(button)
            self.buttons.add(button)

    def handle_events(self):
        """Get and handle events in the pygame event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_screen = "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_screen = "resume"

    def process_next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed."""
        # if "resume" is selected:
        if self.next_screen == "resume":
            # additional steps if resuming
            # calculate the total time paused and save
            self.pause_end = pygame.time.get_ticks()
            self.duration = self.pause_end - self.pause_begin
        # return next screen's name
        return self.next_screen

    def update(self):
        """Handle events and return next screen to display."""
        self.handle_events()

        return self.process_next_screen()

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
