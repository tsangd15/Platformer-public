"""Main game file"""
import sys
import pygame
from _rootmenu import RootMenu
from _level_main import LevelMain
from _level_pause import LevelPause
from _level_complete import LevelComplete
from _level_fail import LevelFail
from _settings import (WINDOW_WIDTH, WINDOW_HEIGHT, GREEN)


def quit_program():
    """Safely and swiftly end the program. Calling pygame.quit() saves a 2
    second wait for the window to close."""
    pygame.quit()
    sys.exit()


class Program():
    """Class to run program's root menu which calls further menus/runs a game
    level."""
    def __init__(self):
        pygame.init()
        self.resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("2D Platformer")

        # clock setup
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()

        self.rootmenu()

    def rootmenu(self):
        """Display the root menu for the player to navigate to different
        screens"""
        item_calls = {"play": self.level_main,              # 0
                      "leaderboard": self.leaderboard,     # 1
                      "tutorial": self.tutorial,           # 2
                      "options": self.options,             # 3
                      "quit": quit_program}                # 4

        # tuple(item_calls) returns only the dictionary keys in a tuple
        # e.g. ("PLAY", "LEADERBOARD")
        menu = RootMenu(tuple(item_calls))

        while True:
            self.clock.tick(25)

            # check if menu item returned, if so, run corresponding function
            # in item_calls dict
            next_screen = menu.update()
            if next_screen is not None:
                item_calls[next_screen]()

            self.screen.fill(GREEN)

            menu.sprites.draw(self.screen)

            pygame.display.flip()

    def level_main(self):
        """Load and run a game level"""
        screen_calls = {"pause": self.level_pause,              # 0
                        "level_complete": self.level_complete,  # 1
                        "level_fail": self.level_fail,          # 2
                        "quit": quit_program}                   # 3
        level = LevelMain(tuple(screen_calls), "test_map")

        while True:
            self.clock.tick(60)

            # check if menu item returned, if so, run corresponding function
            # in item_calls dict
            next_screen = level.update()
            if next_screen is not None:
                if next_screen == "quit":
                    screen_calls[next_screen]()
                elif "level_" in next_screen:
                    screen_calls[next_screen](level.sprites)
                    # return back to root menu
                    return
                else:
                    pause_return = screen_calls[next_screen](level.sprites)

                    # if user requested to go back to root menu
                    if pause_return == "gotoroot":
                        return
                    # otherwise correct cooldowns and resume level
                    level.resume(pause_return)

            self.screen.fill(GREEN)

            level.sprites.draw(self.screen)

            pygame.display.flip()

    def level_pause(self, level_sprites):
        """Display level pause screen"""
        screen_calls = {"resume": None,
                        "options": self.options,
                        "root_menu": None,
                        "quit": quit_program}

        pause = LevelPause(tuple(screen_calls))

        while True:
            self.clock.tick(25)

            next_screen = pause.update()
            if next_screen is not None:
                if next_screen == "quit":
                    screen_calls[next_screen]()
                elif next_screen == "options":
                    # pass game level's sprites again to retain background
                    screen_calls[next_screen](level_sprites)
                elif next_screen == "root_menu":
                    return "gotoroot"
                # resume the level by terminating the method
                else:
                    return pause.duration

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            pause.sprites.draw(self.screen)

            pygame.display.flip()

    def level_complete(self, level_sprites):
        """Display level pause screen"""
        print("ran level_complete()")
        screen_calls = {"quit": quit_program}
        complete = LevelComplete(tuple(screen_calls))

        while True:
            self.clock.tick(25)

            next_screen = complete.update()
            if next_screen is not None:
                screen_calls[next_screen]()

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            complete.sprites.draw(self.screen)

            pygame.display.flip()

    def level_fail(self, level_sprites):
        """Display level pause screen"""
        print("ran level_fail()")
        screen_calls = {"quit": quit_program}
        fail = LevelFail(tuple(screen_calls))

        while True:
            self.clock.tick(25)

            next_screen = fail.update()
            if next_screen is not None:
                screen_calls[next_screen]()

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            fail.sprites.draw(self.screen)

            pygame.display.flip()

    def leaderboard(self):
        """Display game leaderboard screen"""
        print("ran leaderboard()")

    def tutorial(self):
        """Display game tutorial screen"""
        print("ran tutorial()")

    def options(self):
        """Display options screen"""
        print("ran options()")


# instantiate and run program
program = Program()
