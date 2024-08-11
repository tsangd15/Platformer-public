"""Enemy Class Module"""
import pygame
from _entity import Entity, sfx_fire, sfx_hit
from _projectile import Projectile
from _settings import PURPLE
from _enemy_vision import EnemyVision


class Enemy(Entity):
    """Class for enemy"""
    def __init__(self, color, width, height, startx=430, starty=400,
                 vision=150):
        super().__init__(color, width, height, startx, starty)
        self.health = 50
        self.number = 0

        # time to respond to player detection in milliseconds
        self.responsetime = 1000

        # control firerate
        self.firecooldown = 320
        self.lastfired = pygame.time.get_ticks()

        self.vision = EnemyVision(vision)

        # store if enemy is maintaining view of the player
        self.watching = False
        # store time player was first spotted
        self.first_spotted = pygame.time.get_ticks()
        # store vector from enemy to player
        self.vectortoplayer = ()

        self.onplatform = False

    def fire(self, projectile_velocity):
        """Spawns a projectile and adds it to the projectiles sprite group
        attribute."""
        projectile = Projectile(PURPLE, self.rect.centerx,
                                self.rect.centery, projectile_velocity[0],
                                projectile_velocity[1], 5)

        self.projectiles.add(projectile)

        if self.sfx:
            sfx_fire.play()

    def hit(self, amount):
        """Method to reduce health when hit by projectile."""
        self.health -= amount
        print("hit", self.number)
        self.number += 1

        if self.sfx:
            sfx_hit.play()

    def move_horizontally(self):
        """Move the player horizontally."""
        # move right
        if self.movingright:
            self.velocity_x = 4
            # cant be sure player is still on a platform so enable gravity
            self.onplatform = False

        # move left
        if self.movingleft:
            self.velocity_x = -4
            # cant be sure player is still on a platform so enable gravity
            self.onplatform = False

    def move_vertically(self):
        """Move the sprite vertically (jump/fall).

        This method will make the entity jump if its on a platform (i.e.
        onplatform attribute is True) at the time it wants to jump.

        Additionally, this method handles vertical acceleration, in turn,
        handling falling."""
        # jump if on platform
        if self.jumping and self.onplatform:
            self.jumpmomentum = -14
            self.onplatform = False

        if not self.onplatform:
            # apply gravity velocity
            self.jumpmomentum += 1

        # gradually reduce momentum (i.e. upward acceleration decreases) so
        # that when momentum is positive, player begins to fall (pygame y axis
        # is 0 at top of screen so up is negative and down is positive)
        self.velocity_y += self.jumpmomentum

        # cap max velocity due to gravity to 4
        if self.jumpmomentum > 4:
            self.jumpmomentum = 4

    def update_vision(self):
        """Update vision sprite's centre with enemy sprite's centre."""
        self.vision.update_location(self.rect.centerx, self.rect.centery)

    def spotted(self, status, vectortoplayer=None):
        """Update the enemy on if the player has been spotted or not.
        If spotted (status=True) for first time (watching=False), watching is
        set to True, time is recorded to first_spotted and the vector to the
        player updated.

        If spotted (status=True) but already previously spotted (previous
        spotted call was status=True so watching=True) then only the vector to
        the player is updated, first_spotted is unchanged and still holds time
        it first spotted the player.

        If no longer spotted/not spotted (status=False), watching is set to
        False."""
        if status is True:
            if not self.watching:
                self.watching = True
                self.first_spotted = pygame.time.get_ticks()
            # update vector from enemy to player
            self.vectortoplayer = vectortoplayer
        else:
            self.watching = False

    def attack(self):
        """If the enemy has maintained view of the player for at least its
        responsetime's duration and hasn't fired in the last firecooldown's
        duration, fire at player."""
        now = pygame.time.get_ticks()
        if ((now - self.first_spotted > self.responsetime) and
           (now - self.lastfired > self.firecooldown)):
            self.lastfired = now
            self.fire(self.vectortoplayer)
            print("firing!!!")

    def update(self):
        """Method to check if health is below 0, if so, despawn enemy.
        Update sfx attribute to turn on/off sound effects."""
        super().update()

        self.move_horizontally()
        self.move_vertically()

        if self.health <= 0:
            self.vision.kill()
            self.kill()

        self.update_vision()

        # attempt to attack if player in enemy sight
        if self.watching:
            self.attack()
