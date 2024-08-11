"""Player Class Module"""
import pygame
from _entity import Entity
from _projectile import Projectile
from _settings import BLUE


class Player(Entity):
    def __init__(self, color, width, height, startx=430, starty=400):
        super().__init__(color, width, height, startx, starty)
        self.projectileslist = pygame.sprite.Group

    def fire(self):
        projectile = Projectile(BLUE, self.rect.x, self.rect.y, 10, 0)
        return projectile
