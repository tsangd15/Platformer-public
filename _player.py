"""Player Class Module"""
import pygame
from _entity import Entity
from _projectile import Projectile
from _settings import WINDOW_WIDTH, GREEN, RED, YELLOW, PURPLE
from _progressbar import ProgressBar
from _text import Text
from _player_lives import LivesIndicator


class Player(Entity):
    """Class for player"""
    def __init__(self, color, width, height, startx, starty):
        super().__init__(color, width, height, startx, starty)
        self.projectiles = pygame.sprite.Group()
        self.defaulthealth = 25
        self.gameover = False
        self.sprinting = False
        self.firecooldown = 320
        self.lastfired = pygame.time.get_ticks()
        self.lastjumped = pygame.time.get_ticks()
        self.lastsprinted = pygame.time.get_ticks()
        self.number = 0
        self.stats = pygame.sprite.Group()
        self._score = 0
        self.score_text = Text("Score: 0", 25, RED, None, 10, 5)
        self.health = ProgressBar(300, 20, RED, YELLOW, WINDOW_WIDTH/2-150,
                                  5, self.defaulthealth)
        # to make the outline between the two bars consistent:
        # stamina starty = health startx + health height - health outline
        # = 5+20-2 = 23
        self.stamina = ProgressBar(300, 20, GREEN, YELLOW, WINDOW_WIDTH/2-150,
                                   23, 100)
        self.lives = LivesIndicator(560, 24)
        self.stats.add(self.score_text, self.health.bars, self.stamina.bars,
                       self.lives)

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
        self.lives.value -= 1
        self.health.value = self.defaulthealth
        self.rect.x, self.rect.y = self.startx, self.starty

    def update(self):
        self.resetvelocity()

        now = pygame.time.get_ticks()

        if (not(self.jumping and self.sprinting) and
           (now - self.lastjumped >= 1000) and
           (now - self.lastsprinted >= 1000)):
            self.stamina.value += 0.5

        # move left/right if key pressed
        if self.movingright:
            if self.sprinting and self.stamina.value >= 2:
                self.velocity_x = 6
                self.stamina.value -= 2
                self.lastsprinted = now
            else:
                self.velocity_x = 4
                self.sprinting = False
        if self.movingleft:
            if self.sprinting and self.stamina.value >= 2:
                self.velocity_x = -6
                self.stamina.value -= 2
                self.lastsprinted = now
            else:
                self.velocity_x = -4
                self.sprinting = False

        # make player jump as long as they haven't been in the air for longer
        # than 3 frames
        if self.jumping and self.airduration < 2:
            # check if enough stamina and on platform not long ago
            if self.stamina.value >= 5:
                self.jumpmomentum = -14
                self.stamina.value -= 5
                self.lastjumped = now
            else:
                self.jumping = False

        self.velocity_y += self.jumpmomentum
        self.jumpmomentum += 1
        if self.jumpmomentum > 4:
            self.jumpmomentum = 4

        if self.health.value <= 0:
            if self.lives.value <= 0:
                self.gameover = True
                print("GAMEOVER")
            else:
                self.respawn()
                print("RESPAWNED")

    @property
    def score(self):
        """Property decorator for score attribute"""
        return self._score

    @score.setter
    def score(self, new_score):
        self._score = new_score
        self.score_text.text = "Score: " + str(self.score)
