"""Main game file"""
import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GREEN, RED, BLUE
from _platform import Platform
from _player import Player

# --------------- Movement and Collision Functions --------------- #


def list_collisions(sprite, spritelist):
    """Takes in a singular sprite and spritelist
    Returns list of sprites in spritelist that collide with the singular
    sprite."""
    collisionslist = pygame.sprite.spritecollide(sprite, spritelist, False)
    return collisionslist


def move(sprite, platformlist):
    """Method to move specific sprite, taking into account collisions with
    sprites under the provided spritelist.

    Method moves the sprite in the x direction first, then corrects it's
    location if it has collided, then moves the sprite in the y direction
    and corrects if it has collided. Returns the sides it has collided
    with for further conditional actions."""
    detectedcollisions = {
        "left": False,
        "right": False,
        "top": False,
        "bottom": False
        }

    sprite.rect.x += sprite.velocity_x
    collisionslist = list_collisions(sprite, platformlist)
    for platform in collisionslist:
        if sprite.velocity_x < 0:  # sprite left
            sprite.rect.left = platform.rect.right
            detectedcollisions["left"] = True

        elif sprite.velocity_x > 0:  # sprite right
            sprite.rect.right = platform.rect.left
            detectedcollisions["right"] = True

    sprite.rect.y += sprite.velocity_y
    collisionslist = list_collisions(sprite, platformlist)
    for platform in collisionslist:
        if sprite.velocity_y > 0:  # sprite bottom
            sprite.rect.bottom = platform.rect.top
            detectedcollisions["bottom"] = True

        if sprite.velocity_y < 0:  # sprite top
            sprite.rect.top = platform.rect.bottom
            detectedcollisions["top"] = True

    if ((sprite.rect.left > WINDOW_WIDTH) or
       (sprite.rect.right < 0) or
       (sprite.rect.bottom < 0) or
       (sprite.rect.top > WINDOW_HEIGHT)):
        sprite.kill()

    return detectedcollisions


# --------------- Constants --------------- #
PLATFORMLENGTH = 50
# automatically determine number of rows/columns
NUMBEROFCOLUMNS = int(WINDOW_WIDTH/PLATFORMLENGTH)
NUMBEROFROWS = int(WINDOW_HEIGHT/PLATFORMLENGTH)


class Game():
    """Class to run game instance"""
    def __init__(self):
        pygame.init()
        self.resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("2D Platformer")

        # 0 = nothing
        # 1 = platform
        self.gamemap = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
                ]

        # Setting up sprite lists
        self.sprites = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # Creating sprites then adding to sprite lists
        self.player = Player(BLUE, 40, 70)
        self.sprites.add(self.player)
        self.entities.add(self.player)

        for row in range(NUMBEROFROWS):
            for col in range(NUMBEROFCOLUMNS):

                if self.gamemap[row][col] == 1:  # platforms
                    plat = Platform(RED, PLATFORMLENGTH, PLATFORMLENGTH)
                    plat.setlocation(col*PLATFORMLENGTH, row*PLATFORMLENGTH)
                    self.sprites.add(plat)
                    self.platforms.add(plat)

    def moveprojectiles(self):
        """Iterates through each projectile in each entity's 'projectiles'
        sprite group attribute and moves them using their stored velocity, if
        they collide with a platform or go off screen, it is despawned."""
        for entity in self.entities:
            for projectile in entity.projectiles:
                collisions = move(projectile, self.platforms)
                if True in collisions.values():
                    projectile.kill()
            entity.projectiles.draw(self.screen)

    def rungame(self):
        """Run Main Game"""
        # game running flag
        run = True

        # clock setup
        clock = pygame.time.Clock()

        # game loop
        while run:

            clock.tick(FPS)

            # keybind detection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        run = False
                    if event.key == pygame.K_a:
                        self.player.movingleft = True
                    if event.key == pygame.K_d:
                        self.player.movingright = True
                    if event.key == pygame.K_w:
                        self.player.jumping = True
                    if event.key == pygame.K_SPACE:
                        self.player.fire()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.movingleft = False
                    if event.key == pygame.K_d:
                        self.player.movingright = False
                    if event.key == pygame.K_w:
                        self.player.jumping = False

            # --------------- game logic ------------- #
            self.screen.fill(GREEN)

            # call update function for each sprite in sprites list
            self.sprites.update()

            # move player
            collisions = move(self.player, self.platforms)
            if collisions["bottom"]:
                self.player.jumpmomentum = 0
                self.player.airduration = 0
            else:
                self.player.airduration += 1

            # if player top collides, momentum reset
            if collisions["top"]:
                self.player.jumpmomentum = 0

            # move projectiles
            self.moveprojectiles()

            self.sprites.draw(self.screen)

            # update the screen
            pygame.display.flip()

        pygame.quit()


game = Game()
game.rungame()
