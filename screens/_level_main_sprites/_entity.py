"""Entity Class Module"""
import pygame
from utils._settings import BLACK
from utils._config_handler import load_config


# --------------- Sound Objects --------------- #
pygame.mixer.init()
sfx_fire = pygame.mixer.Sound("assets/SFX_Fire.wav")
sfx_hit = pygame.mixer.Sound("assets/SFX_Hit.wav")
sfx_respawn = pygame.mixer.Sound("assets/SFX_Respawn.wav")

sfx_fire.set_volume(0.35)
sfx_hit.set_volume(0.35)
sfx_respawn.set_volume(0.35)


class Entity(pygame.sprite.Sprite):
    """Class to inherit from for player and NPC sprites. Not to be directly
    used to create objects."""
    def __init__(self, color, width, height, startx, starty):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color

        # instantiate projectiles sprite group
        self.projectiles = pygame.sprite.Group()

        # draw the square
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        # set start pos and save spawn pos
        self.startx = startx
        self.starty = starty
        self.rect.x = self.startx
        self.rect.y = self.starty

        # defining attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.movingleft = False
        self.movingright = False
        self.jumping = False
        self.jumpmomentum = 0
        self.onplatform = False

        # turn on/off sound effects (sfx)
        self.check_sfx_setting()

    def resetvelocity(self):
        """Resets player velocity"""
        self.velocity_x = 0
        self.velocity_y = 0

    def check_sfx_setting(self):
        """Reads the sound_effects key from config.json and saves it to self.sfx.
        If self.sfx is True, sound effects should be played, otherwise they
        shouldn't."""
        self.sfx = load_config()["sound_effects"]

    def update(self):
        """Update method to carry out actions for entity each game loop.
        Method called via sprites.update()
        Resets velocity."""
        self.resetvelocity()
