"""Enemy Class Module"""
from _entity import Entity, sfx_hit


class Enemy(Entity):
    """Class for enemy"""
    def __init__(self, color, width, height, startx=430, starty=400):
        super().__init__(color, width, height, startx, starty)
        self.health = 50
        self.number = 0

    def hit(self):
        """Method to reduce health when hit by projectile."""
        self.health -= 5
        print("hit", self.number)
        self.number += 1

        if self.sfx:
            sfx_hit.play()

    def update(self):
        """Method to check if health is below 0, if so, despawn enemy.
        Update sfx attribute to turn on/off sound effects."""
        self.check_sfx_setting()

        if self.health <= 0:
            self.kill()
