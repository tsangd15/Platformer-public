"""Player Class Module"""
import pygame
from ._entity import Entity, sfx_fire, sfx_hit, sfx_respawn
from ._projectile import Projectile
from utils._settings import WINDOW_WIDTH, GREEN, RED, YELLOW, PURPLE
from utils._progressbar import ProgressBar
from utils._text import Text
from ._player_lives import LivesIndicator


class Player(Entity):
    """Class for player"""
    def __init__(self, color, width, height, startx, starty):
        super().__init__(color, width, height, startx, starty)
        self.defaulthealth = 25
        self.defaultstamina = 100
        self.dead = False
        self.sprinting = False

        # ------ COOLDOWNS AND LAST EVENTS ------ #
        self.firecooldown = 320
        self.staminacooldown_jump = 2500
        self.staminacooldown_sprint = 1500
        self.healthcooldown = 7000
        self.lastfired = pygame.time.get_ticks()
        self.lastjumped = pygame.time.get_ticks()
        self.lastsprinted = pygame.time.get_ticks()
        self.lasthit = pygame.time.get_ticks()

        # for hit debugging
        self.number = 0

        # ------ STATS PANEL ------ #
        self.stats = pygame.sprite.Group()
        self._score = 0
        self.score_text = Text("Score: 0", 25, "top_left", RED, None, 10, 5)
        self.health = ProgressBar(300, 20, RED, YELLOW, WINDOW_WIDTH/2-150,
                                  5, self.defaulthealth)
        # to make the outline between the two bars consistent:
        # stamina starty = health startx + health height - health outline
        # = 5+20-2 = 23
        self.stamina = ProgressBar(300, 20, GREEN, YELLOW, WINDOW_WIDTH/2-150,
                                   23, self.defaultstamina)
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
                                    projectile_velocity[1], 5)

            self.projectiles.add(projectile)

            if self.sfx:
                sfx_fire.play()

    def hit(self, amount):
        """Method to reduce health when hit by projectile."""
        now = pygame.time.get_ticks()
        self.lasthit = now

        self.health.value -= amount

        self.number += 1

        if self.sfx:
            sfx_hit.play()

    def respawn(self):
        """Decrease lives, reset health & stamina and teleport to spawn
        location for respawn."""
        self.lives.value -= 1
        self.health.value = self.defaulthealth
        self.stamina.value = self.defaultstamina
        self.rect.x, self.rect.y = self.startx, self.starty

        # cant be sure player is still on a platform so enable gravity
        self.onplatform = False

        if self.sfx:
            sfx_respawn.play()

    def replenish_health(self, now):
        """Replenish health slowly if player hasn't taken damage for the
        duration of self.healthcooldown."""
        if now - self.lasthit >= self.healthcooldown:
            self.health.value += 0.01

    def replenish_stamina(self, now):
        """Replenish stamina if player hasn't sprinted/jumped for respective
        cooldown duration."""
        if (not(self.jumping and self.sprinting) and
           (now - self.lastjumped >= self.staminacooldown_jump) and
           (now - self.lastsprinted >= self.staminacooldown_sprint)):
            self.stamina.value += 0.5

    def move_2d(self, now):
        """Move the sprite horizontally (left/right) and vertically (jump/fall).

        This method will make the entity jump if its on a platform (i.e.
        onplatform attribute is True) at the time it wants to jump.

        Additionally, this method handles vertical acceleration, in turn,
        handling falling."""
        # jump if on platform
        if self.jumping and self.onplatform:
            # check if enough stamina
            if self.stamina.value >= 5:
                self.jumpmomentum = -16
                self.onplatform = False
                self.stamina.value -= 5
                self.lastjumped = now
            else:
                # reset jump so stamina can regen fully
                self.jumping = False

        # move right
        if self.movingright:
            # check if sprint key down and sufficient stamina
            if self.sprinting and self.stamina.value >= 2:
                self.velocity_x = 6
                self.stamina.value -= 2
                self.lastsprinted = now
            # otherwise move at default velocity
            else:
                self.velocity_x = 4
                # reset sprint so stamina can regen fully
                self.sprinting = False

            # cant be sure player is still on a platform so enable gravity
            self.onplatform = False

        # move left
        if self.movingleft:
            # check if sprint key down and sufficient stamina
            if self.sprinting and self.stamina.value >= 2:
                self.velocity_x = -6
                self.stamina.value -= 2
                self.lastsprinted = now
            # otherwise move at default velocity
            else:
                self.velocity_x = -4
                # reset sprint so stamina can regen fully
                self.sprinting = False

            # cant be sure player is still on a platform so enable gravity
            self.onplatform = False

        if not self.onplatform:
            # apply gravity velocity
            self.jumpmomentum += 1

        # gradually reduce momentum (i.e. upward acceleration decreases) so
        # that when momentum is positive, player begins to fall (pygame y axis
        # is 0 at top of screen so up is negative and down is positive)
        self.velocity_y += self.jumpmomentum

        # cap max velocity due to gravity to 4
        # min function returns smallest of arguments passed
        self.jumpmomentum = min(self.jumpmomentum, 4)

    def is_health_depleted(self):
        """Check if player health is depleted. If so invokes respawn if
        sufficient lives, otherwise declare game is over."""
        # check health depleted
        if self.health.value <= 0:
            # check for insufficient lives
            if self.lives.value <= 0:
                self.dead = True
            else:
                self.respawn()

    def regulate_cooldown(self, time_paused):
        """Adjust the lastfired, lastjumped, lastsprinted and lasthit
        attributes to account for the time paused as if the game was never
        paused."""
        self.lastfired = self.lastfired + time_paused
        self.lastjumped = self.lastjumped + time_paused
        self.lastsprinted = self.lastsprinted + time_paused
        self.lasthit = self.lasthit + time_paused

    def update(self):
        """Carry out operations to update player's location and attributes
        like health and stamina."""
        super().update()

        now = pygame.time.get_ticks()

        self.replenish_health(now)

        self.replenish_stamina(now)

        self.move_2d(now)

        self.is_health_depleted()

    @property
    def score(self):
        """Property decorator for score attribute"""
        return self._score

    @score.setter
    def score(self, new_score):
        """Setter for score attribute to auto update text on score change"""
        self._score = new_score
        # update score text sprite
        self.score_text.text = "Score: " + str(self.score)
