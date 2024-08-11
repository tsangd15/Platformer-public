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
        self.lastfired = pygame.time.get_ticks()
        self.firecooldown = 500

    def fire(self):
        """Spawns a projectile and adds it to the projectiles sprite group
        attribute."""
        now = pygame.time.get_ticks()
        if now - self.lastfired >= self.firecooldown:
            self.lastfired = now

            if self.movingleft:
                projectile_velocity_x = -10
            else:
                projectile_velocity_x = 10

            projectile = Projectile(BLUE, self.rect.x, self.rect.y,
                                    projectile_velocity_x, 0)
            self.projectiles.add(projectile)
