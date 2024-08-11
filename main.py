"""Main game file"""
import sys
import pygame
from _rootmenu import RootMenu
from _level_main import LevelMain
from _level_pause import LevelPause
from _level_complete import LevelComplete
from _level_fail import LevelFail
from _leaderboard import Leaderboard
from _save_score import SaveScore
from _options import Options
from _settings import (WINDOW_WIDTH, WINDOW_HEIGHT, GREEN, BLACK)
from _config_handler import load_config


def quit_program():
    """Safely and swiftly end the program. Calling pygame.quit() saves a 2
    second wait for the window to close."""
    pygame.quit()
    sys.exit()


class Program():
    """Class to run game program. This class handles the pygame screen surface,
    clock and what screen is running currently and blits its sprites on its
    behalf."""
    def __init__(self):
        pygame.init()

        # load and play music
        pygame.mixer.music.load("assets/MUSIC_Adventure_AlexanderNakarada.mp3")
        pygame.mixer.music.set_volume(0.3)
        if load_config()["music"]:
            pygame.mixer.music.play(-1)

        # screen surface setup
        self.resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("2D Platformer")

        # clock setup
        self.clock = pygame.time.Clock()

        # display root menu screen
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
                    screen_return = (screen_calls[next_screen]
                                     (level.sprites, level.player.score))
                    # if the user requested to go back to root menu
                    if screen_return == "gotoroot":
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

        # create transparent background
        background = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        background.fill(GREEN)
        background.set_alpha(200)

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

            # draw background on top of level sprites
            self.screen.blit(background.convert_alpha(), (0, 0))

            pause.sprites.draw(self.screen)

            pygame.display.flip()

    def level_complete(self, level_sprites, score):
        """Display level pause screen"""
        print("ran level_complete()")
        screen_calls = {"save_score": self.save_score,
                        "root_menu": None,
                        "quit": quit_program}
        complete = LevelComplete(tuple(screen_calls), score)

        # create transparent background
        background = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        background.fill(GREEN)
        background.set_alpha(200)

        while True:
            self.clock.tick(25)

            next_screen = complete.update()
            if next_screen is not None:
                if next_screen == "save_score":
                    screen_return = screen_calls[next_screen](level_sprites,
                                                              score)
                    if screen_return == "gotoroot":
                        return "gotoroot"
                elif next_screen == "root_menu":
                    return "gotoroot"
                else:
                    screen_calls[next_screen]()

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            # draw background on top of level sprites
            self.screen.blit(background.convert_alpha(), (0, 0))

            complete.sprites.draw(self.screen)

            pygame.display.flip()

    def level_fail(self, level_sprites, score):
        """Display level pause screen"""
        print("ran level_fail()")
        screen_calls = {"save_score": self.save_score,
                        "root_menu": None,
                        "quit": quit_program}
        fail = LevelFail(tuple(screen_calls), score)

        # create transparent background
        background = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        background.fill(GREEN)
        background.set_alpha(200)

        while True:
            self.clock.tick(25)

            next_screen = fail.update()
            if next_screen is not None:
                if next_screen == "save_score":
                    screen_return = screen_calls[next_screen](level_sprites,
                                                              score)
                    if screen_return == "gotoroot":
                        return "gotoroot"
                elif next_screen == "root_menu":
                    return "gotoroot"
                else:
                    screen_calls[next_screen]()

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            # draw background on top of level sprites
            self.screen.blit(background.convert_alpha(), (0, 0))

            fail.sprites.draw(self.screen)

            pygame.display.flip()

    def save_score(self, level_sprites, score):
        """Display save score screen"""
        print("ran save_score()")
        screen_calls = {"global_save": None,
                        "local_save": None,
                        "root_menu": None,
                        "quit": quit_program}
        save_score = SaveScore(tuple(screen_calls), score)

        # create transparent background
        background = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        background.fill(GREEN)
        background.set_alpha(200)

        while True:
            self.clock.tick(25)

            # check if menu item returned, if so, run corresponding function
            # in item_calls dict
            next_screen = save_score.update()
            if next_screen is not None:
                if next_screen == "root_menu":
                    return "gotoroot"
                if next_screen == "quit":
                    screen_calls[next_screen]()
                elif next_screen == "local_save":
                    save_score.save()

            self.screen.fill(GREEN)

            level_sprites.draw(self.screen)

            # draw background on top of level sprites
            self.screen.blit(background.convert_alpha(), (0, 0))

            save_score.sprites.draw(self.screen)

            pygame.display.flip()

    def leaderboard(self):
        """Display game leaderboard screen"""
        screen_calls = {"root_menu": None,
                        "quit": quit_program}
        leaderboard = Leaderboard(tuple(screen_calls))

        while True:
            self.clock.tick(25)

            # check if menu item returned, if so, run corresponding function
            # in item_calls dict
            next_screen = leaderboard.update()
            if next_screen is not None:
                if next_screen == "quit":
                    screen_calls[next_screen]()
                else:
                    return

            self.screen.fill(GREEN)

            leaderboard.sprites.draw(self.screen)

            pygame.display.flip()

    def tutorial(self):
        """Display game tutorial screen"""
        print("ran tutorial()")

    def options(self, level_sprites=None):
        """Display options screen"""
        screen_calls = {"quit": quit_program,
                        "back": None,
                        "config_music": None,
                        "config_sound_effects": None}
        options = Options(tuple(screen_calls))
        screen_calls["config_music"] = options.config_music
        screen_calls["config_sound_effects"] = options.config_sound_effects

        # create transparent background
        background = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        background.fill(BLACK)
        background.set_alpha(200)

        while True:
            self.clock.tick(25)

            # check if menu item returned, if so, run corresponding function
            # in item_calls dict
            next_screen = options.update()
            if next_screen is not None:
                if next_screen == "quit":
                    screen_calls[next_screen]()
                elif next_screen == "back":
                    return
                elif "config_" in next_screen:
                    screen_calls[next_screen]()

            self.screen.fill(BLACK)

            # display level sprites if provided
            if level_sprites is not None:
                level_sprites.draw(self.screen)

                # draw background on top of level sprites
                self.screen.blit(background.convert_alpha(), (0, 0))

            options.sprites.draw(self.screen)

            pygame.display.flip()


# instantiate and run program
program = Program()
