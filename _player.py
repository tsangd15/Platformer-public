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
        self.firecooldown = 320

    def fire(self, projectile_velocity):
        """Spawns a projectile and adds it to the projectiles sprite group
        attribute."""
        now = pygame.time.get_ticks()
        if now - self.lastfired >= self.firecooldown:
            self.lastfired = now

            projectile = Projectile(BLUE, self.rect.centerx,
                                    self.rect.centery, projectile_velocity[0],
                                    projectile_velocity[1])

            self.projectiles.add(projectile)
