"""Entity Class Module"""
import pygame
from _settings import BLACK


class Entity(pygame.sprite.Sprite):
    """Class to inherit from for player and NPC sprites. Not to be directly
    used to create objects."""
    def __init__(self, color, width, height, startx, starty):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)  # greenscreen effect for images
        self.color = color

        # draw the square
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.rect.x = startx
        self.rect.y = starty
        self.velocity_x = 0
        self.velocity_y = 0
        self.movingleft = False
        self.movingright = False
        self.jumping = False
        self.jumpmomentum = 0
        self.airduration = 0

    def resetvelocity(self):
        """Resets player velocity"""
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        """Update method to carry out actions for entity each game loop.
        Method called via sprites.update()
        Resets velocity and alters velocity accordingly depending on the
        remaining vertical momentum and if it should still be moving left/
        right (i.e. left key still pressed)."""
        self.resetvelocity()

        if self.movingright:
            self.velocity_x = 4
        if self.movingleft:
            self.velocity_x = -4
        # make player jump as long as they haven't been in the air for longer
        # than 3 frames
        if self.jumping:
            if self.airduration < 2:
                self.jumpmomentum = -14

        self.velocity_y += self.jumpmomentum
        self.jumpmomentum += 1
        if self.jumpmomentum > 4:
            self.jumpmomentum = 4
