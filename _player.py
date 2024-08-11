"""Player Class Module"""
import pygame
from _entity import Entity
from _projectile import Projectile
from _settings import BLUE


class Player(Entity):
    """Class for player"""
    def __init__(self, color, width, height, startx=430, starty=400):
        super().__init__(color, width, height, startx, starty)
        self.projectiles = pygame.sprite.Group()

    def fire(self):
        """Spawns a projectile and adds it to the projectiles sprite group
        attribute."""
        projectile = Projectile(BLUE, self.rect.x, self.rect.y, 10, 0)
        self.projectiles.add(projectile)
