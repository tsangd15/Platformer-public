"""Enemy Class Module"""
from _entity import Entity, sfx_fire, sfx_hit
from _projectile import Projectile
from _settings import PURPLE
from _enemy_vision import EnemyVision


class Enemy(Entity):
    """Class for enemy"""
    def __init__(self, color, width, height, startx=430, starty=400,
                 vision=100):
        super().__init__(color, width, height, startx, starty)
        self.health = 50
        self.number = 0

        self.vision = EnemyVision(vision)

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

        # move left
        if self.movingleft:
            self.velocity_x = -4

    def move_vertically(self):
        """Move the sprite vertically (jump/fall).

        This method will make the entity jump if its on a platform or just
        recently (2 frames) left the ground.

        Additionally, this method handles vertical acceleration, in turn,
        handling falling."""
        # jump as long as they haven't been in the air for longer than 2 frames
        if self.jumping and self.airduration < 2:
            self.jumpmomentum = -14

        # gradually reduce momentum (i.e. upward acceleration decreases) so
        # that when momentum is positive, player begins to fall (pygame y axis
        # is 0 at top of screen so up is negative and down is negative)
        self.velocity_y += self.jumpmomentum
        self.jumpmomentum += 1
        if self.jumpmomentum > 4:
            self.jumpmomentum = 4

    def update_vision(self):
        """Update vision sprite's centre with enemy sprite's centre."""
        self.vision.update_location(self.rect.centerx, self.rect.centery)

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
