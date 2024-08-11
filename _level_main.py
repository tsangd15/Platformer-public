"""Game Level - Main Module"""
from math import sqrt
import pygame
from _settings import (WINDOW_WIDTH, WINDOW_HEIGHT, RED, BLUE, PINK, YELLOW)
from _platform import Platform
from _player import Player
from _enemy import Enemy


def list_collisions(sprite, spritelist):
    """Input singular sprite and spritelist
    Returns list of sprites in spritelist that collide with the singular
    sprite."""
    collisionslist = pygame.sprite.spritecollide(sprite, spritelist, False)
    return collisionslist


def list_groupcollisions(group1, group2):
    """Returns collisions between sprites in two sprite groups.
    Returns dictionary with each sprite in group1 that collided as a key and
    each sprite in group2 that collided as a value for the respective sprite
    it collided with in group1. key:value"""
    collisionslist = pygame.sprite.groupcollide(group1, group2, False, False)
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

    # horizontal movement handling
    sprite.rect.x += sprite.velocity_x
    collisionslist = list_collisions(sprite, platformlist)
    for platform in collisionslist:
        if sprite.velocity_x < 0:  # sprite left
            sprite.rect.left = platform.rect.right
            detectedcollisions["left"] = True

        elif sprite.velocity_x > 0:  # sprite right
            sprite.rect.right = platform.rect.left
            detectedcollisions["right"] = True

    # vertical movement handling
    sprite.rect.y += sprite.velocity_y
    collisionslist = list_collisions(sprite, platformlist)
    for platform in collisionslist:
        if sprite.velocity_y > 0:  # sprite bottom
            sprite.rect.bottom = platform.rect.top
            detectedcollisions["bottom"] = True

        if sprite.velocity_y < 0:  # sprite top
            sprite.rect.top = platform.rect.bottom
            detectedcollisions["top"] = True

    # kill sprite if offscreen and not player
    if ((sprite.rect.left > WINDOW_WIDTH) or
       (sprite.rect.right < 0) or
       (sprite.rect.bottom < 0) or
       (sprite.rect.top > WINDOW_HEIGHT)):
        if not isinstance(sprite, Player):
            sprite.kill()
        # if player, check if 200 pixels below screen
        else:
            if sprite.rect.top > WINDOW_HEIGHT+200:
                # kill player by deducting significant health
                sprite.hit(200)

    return detectedcollisions


def vector(origin, destination, magnitude):
    """Function to create velocity vectors from 2 points and magnitude.

    Initial vector and magnitude is calculated. Unit vector (vector with
    magnitude 1) is generated and then desired magnitude applied and returned.

    Inputs:
    origin - originating location
    destination - final location
    magnitude - preferred magnitude of output vector (to regulate speed)

    Outputs:
    vector_final - component vector with desired direction and magnitude"""
    changein_x = destination[0] - origin[0]
    changein_y = destination[1] - origin[1]

    vector_initial = [changein_x, changein_y]

    # find initial magnitude using pythagoras (a^2 + b^2 = c^2)
    magnitude_initial = sqrt((changein_x) ** 2 +
                             (changein_y) ** 2)

    # unit vector = vector / magnitude
    unit_vector = [vector_initial[0] / magnitude_initial,
                   vector_initial[1] / magnitude_initial]

    # calculate vector with requested magnitude
    vector_final = [unit_vector[0] * magnitude,
                    unit_vector[1] * magnitude]

    return vector_final


# --------------- Constants --------------- #
PLATFORMLENGTH = 50
# automatically determine number of rows/columns
NUMBEROFCOLUMNS = int(WINDOW_WIDTH/PLATFORMLENGTH)
NUMBEROFROWS = int(WINDOW_HEIGHT/PLATFORMLENGTH)


class LevelMain():
    """Class for running an individual game level"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, screens):
        # import map as 2d array
        self.load_map()

        # Setting up sprite lists
        self.allsprites = pygame.sprite.Group()  # TEMPORARY SPRITE GROUP
        self.sprites = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.finishpoints = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.screens = screens
        self.next_screen_index = -1

        self.paused = False

        self.draw_map()

        self.update_cursor()

    def load_map(self):
        """Load level map as 2D array"""
        # 0 = nothing
        # 1 = platform
        # 2 = player spawn location
        # 3 map finish location
        self.gamemap = []

        # read the map
        with open("maps/test_map.txt", "r") as file:
            # store each line as an element in a list
            lines = file.readlines()
            for i, line in enumerate(lines):
                # remove newline character
                lines[i] = line.replace("\n", "")

        # generate each inner list (row) of 2d list and add to outer list
        for line in lines:
            row = []
            for char in line:
                row.append(int(char))
            self.gamemap.append(row)

    def draw_map(self):
        """Iterate through map and draw each sprite (e.g. platforms, player,
        enemies...)"""
        # Creating sprites then adding to sprite lists
        self.enemy = Enemy(YELLOW, 80, 80)

        self.allsprites.add(self.enemy)
        self.sprites.add(self.enemy)
        self.enemies.add(self.enemy)

        for row in range(NUMBEROFROWS):
            for col in range(NUMBEROFCOLUMNS):

                if self.gamemap[row][col] == 1:  # platforms
                    # colour, width, height, xpos, ypos
                    plat = Platform(RED, PLATFORMLENGTH, PLATFORMLENGTH,
                                    col*PLATFORMLENGTH, row*PLATFORMLENGTH)
                    self.allsprites.add(plat)
                    self.sprites.add(plat)
                    self.platforms.add(plat)

                elif self.gamemap[row][col] == 2:  # player
                    self.player = Player(BLUE, 40, 70, col*PLATFORMLENGTH,
                                         row*PLATFORMLENGTH)
                    self.allsprites.add(self.player, self.player.stats)
                    self.sprites.add(self.player)
                    self.entities.add(self.player)

                elif self.gamemap[row][col] == 3:  # finish point
                    self.finishpoint = Platform(PINK, PLATFORMLENGTH,
                                                PLATFORMLENGTH,
                                                col*PLATFORMLENGTH,
                                                row*PLATFORMLENGTH)
                    self.allsprites.add(self.finishpoint)
                    self.sprites.add(self.finishpoint)
                    self.finishpoints.add(self.finishpoint)

    def moveplayer(self):
        """Uses the move function to move the player sprite by its current
        velocity vector. Collisions with platforms are detected and reacted to.
        If player bottom collides with platform, jumping stops, air duration is
        reset; otherwise air duration is incremented. If player top collides
        with platform, jump momentum reset so they begin falling back down."""
        collisions = move(self.player, self.platforms)
        if collisions["bottom"]:
            self.player.jumpmomentum = 0
            self.player.airduration = 0
        else:
            self.player.airduration += 1

        # if player top collides, momentum reset
        if collisions["top"]:
            self.player.jumpmomentum = 0

    def moveprojectiles(self):
        """Iterates through each projectile in each entity's 'projectiles'
        sprite group attribute and moves them using their stored velocity. If
        the projectile moves off screen, collides with a platform or enemy, it
        is despawned. Damage inflicted on enemy if enemy collision."""
        for entity in self.entities:
            for projectile in entity.projectiles:
                # --- move projectile and/or kill if platform collision --- #
                collisions = move(projectile, self.platforms)
                if True in collisions.values():
                    # kill projectile if it hits a platform
                    projectile.kill()

            # --- kill projectile on enemy collision and inflict damage --- #
            damage = list_groupcollisions(entity.projectiles, self.enemies)
            # iterate through each item (key, value) in dictionary
            for item in damage.items():
                item[0].kill()  # for each projectile (key), kill/despawn

                for key in item[1]:  # iterate through each value
                    key.hit()  # for each enemy in the value, inflict hit
                    self.player.score += 5

            self.allsprites.add(entity.projectiles)

    def check_finish(self):
        """Method to check if the level is finished (completed/failed).
        If player collides with finish points, level completed.
        If player dead attribute true, level failed."""
        if list_collisions(self.player, self.finishpoints) != []:
            self.next_screen_index = 1  # self.screens[1] = "level_complete"
        elif self.player.dead:
            self.next_screen_index = 2  # self.screens[2] = "level_fail"

    def resume(self, pause_duration):
        """Method to properly resume the game after a game pause."""
        self.paused = False
        self.player.regulate_cooldown(pause_duration)
        # reset next screen to null
        self.next_screen_index = -1

    def update_cursor(self):
        """Updates the cursor's stored location"""
        # store current cursor location
        self.cursor = pygame.mouse.get_pos()

    def handle_events(self):
        """Get and handle events in the pygame event queue."""
        # keybind detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_screen_index = 3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.next_screen_index = 0
                if event.key == pygame.K_x:  # X: end program
                    self.next_screen_index = 3
                if event.key == pygame.K_LSHIFT:  # L Shift: sprint
                    self.player.sprinting = True
                if event.key == pygame.K_a:  # A: move left
                    self.player.movingleft = True
                if event.key == pygame.K_d:  # D: move right
                    self.player.movingright = True
                if event.key == pygame.K_w:  # W: jump
                    self.player.jumping = True
                if event.key == pygame.K_SPACE:  # Spacebar: shoot
                    # generate velocity vector from player to cursor
                    projectile_vector = vector(self.player.rect.center,
                                               self.cursor, 10)
                    # spawn projectile with generated velocity
                    self.player.fire(projectile_vector)
                if event.key == pygame.K_h:
                    self.player.hit(5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:  # L Shift: stop sprint
                    self.player.sprinting = False
                if event.key == pygame.K_a:  # A: stop moving left
                    self.player.movingleft = False
                if event.key == pygame.K_d:  # D: stop moving right
                    self.player.movingright = False
                if event.key == pygame.K_w:  # W: stop jumping
                    self.player.jumping = False

            # if event.type == pygame.
            # MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION.

    def next_screen(self):
        """Return the next screen to display (returning None will mean the
        current screen will continue to be displayed."""
        if self.next_screen_index != -1:
            return self.screens[self.next_screen_index]
        return None

    def update(self):
        """Update the cursor and sprites and check if the game is finished."""

        self.update_cursor()

        self.handle_events()

        # call update function for each sprite in sprites list
        self.sprites.update()

        # move player
        self.moveplayer()

        # move projectiles
        self.moveprojectiles()

        # check for game finish
        self.check_finish()

        return self.next_screen()
