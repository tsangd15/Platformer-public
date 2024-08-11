"""Player Class Module"""
import pygame
from _entity import Entity
from _projectile import Projectile
from _settings import WINDOW_WIDTH, GREEN, RED, YELLOW, PURPLE
from _progressbar import ProgressBar


class Player(Entity):
    """Class for player"""
    def __init__(self, color, width, height, startx, starty):
        super().__init__(color, width, height, startx, starty)
        self.projectiles = pygame.sprite.Group()
        self.defaulthealth = 25
        self.lives = 3
        self.gameover = False
        self.lastfired = pygame.time.get_ticks()
        self.firecooldown = 320
        self.number = 0
        self.stats = pygame.sprite.Group()
        self.health = ProgressBar(300, 20, RED, YELLOW, WINDOW_WIDTH/2-150,
                                  20, self.defaulthealth)
        self.stamina = ProgressBar(300, 20, GREEN, YELLOW, WINDOW_WIDTH/2-150,
                                   40, 100)
        self.stats.add(self.health.bars, self.stamina.bars)

    def fire(self, projectile_velocity):
        """Spawns a projectile and adds it to the projectiles sprite group
        attribute."""
        now = pygame.time.get_ticks()
        if now - self.lastfired >= self.firecooldown:
            self.lastfired = now

            projectile = Projectile(PURPLE, self.rect.centerx,
                                    self.rect.centery, projectile_velocity[0],
                                    projectile_velocity[1])

            self.projectiles.add(projectile)

    def hit(self):
        """Method to reduce health when hit by projectile."""
        self.health.value -= 5
        print("hit", self.number)
        self.number += 1

    def respawn(self):
        """Decrease lives and reset health for respawn."""
        self.lives -= 1
        self.health.value = self.defaulthealth
        self.rect.x, self.rect.y = self.startx, self.starty

    def update(self):
        super().update()

        if self.lives < 0:
            self.gameover = True
            print("GAMEOVER")
        else:
            if self.health.value <= 0:
                self.respawn()
                print("RESPAWNED")
