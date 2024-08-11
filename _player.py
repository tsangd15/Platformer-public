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

    def replenish_stamina(self, now):
        """Replenish stamina if player hasn't sprinted/jumped for 1 second."""
        if (not(self.jumping and self.sprinting) and
           (now - self.lastjumped >= 1000) and
           (now - self.lastsprinted >= 1000)):
            self.stamina.value += 0.5

    def move_horizontally(self, now):
        """Move the player horizontally if key pressed. If sprinting and
        sufficient stamina, player will move at sprint velocity; otherwise
        player will move at default velocity."""
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

    def move_vertically(self, now):
        """Move the player vertically (jump/fall).

        This method will make the player jump if jump key is pressed and
        player sprite is on a platform or just recently (2 frames) left the
        ground. Sufficient stamina is required to jump.

        Additionally, this method handles vertical acceleration, in turn,
        handling falling."""
        # make player jump as long as they haven't been in the air for longer
        # than 2 frames
        if self.jumping and self.airduration < 2:
            # additional if statement so that jumping and airduration
            # conditions above don't invoke the else statement

            # check if enough stamina and on platform not long ago
            if self.stamina.value >= 5:
                self.jumpmomentum = -14
                self.stamina.value -= 5
                self.lastjumped = now
            else:
                # reset jump so stamina can regen fully
                self.jumping = False

        # gradually reduce momentum (i.e. upward acceleration decreases) so
        # that when momentum is positive, player begins to fall (pygame y axis
        # is 0 at top of screen so up is negative and down is negative)
        self.velocity_y += self.jumpmomentum
        self.jumpmomentum += 1
        if self.jumpmomentum > 4:
            self.jumpmomentum = 4

    def is_health_depleted(self):
        """Check if player health is depleted. If so invokes respawn if
        sufficient lives, otherwise declare game is over."""
        # check health depleted
        if self.health.value <= 0:
            # check for insufficient lives
            if self.lives.value <= 0:
                self.gameover = True
                print("GAMEOVER")
            else:
                self.respawn()
                print("RESPAWNED")

    def update(self):
        self.resetvelocity()

        now = pygame.time.get_ticks()

        self.replenish_stamina(now)

        self.move_horizontally(now)

        self.move_vertically(now)

        self.is_health_depleted()

    @property
    def score(self):
        """Property decorator for score attribute"""
        return self._score

    @score.setter
    def score(self, new_score):
        self._score = new_score
        self.score_text.text = "Score: " + str(self.score)
