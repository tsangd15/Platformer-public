"""Game Level - Main Module"""
from math import sqrt
import pygame
from _screen import Screen
from _settings import (WINDOW_WIDTH, WINDOW_HEIGHT, RED, BLUE, PINK, YELLOW)
from _platform import Platform
from _player import Player
from _enemy import Enemy
from _projectile import Projectile
from _line import Line


def list_collisions(sprite, spritelist):
    """Input singular sprite and spritelist
    Returns list of sprites in spritelist that collide with the singular
    sprite using their rects."""
    collisionslist = pygame.sprite.spritecollide(sprite, spritelist, False)
    return collisionslist


def list_groupcollisions(group1, group2):
    """Returns collisions between sprites in two sprite groups.
    Returns dictionary with each sprite in group1 that collided as a key and
    each sprite in group2 that collided as a value for the respective sprite
    it collided with in group1. key:value"""
    collisionslist = pygame.sprite.groupcollide(group1, group2, False, False)
    return collisionslist


def list_collisions_mask(sprite, spritelist):
    """Input singular sprite and spritelist
    Returns list of sprites in spritelist that collide with the singular
    sprite using their masks."""
    collisionslist = pygame.sprite.spritecollide(sprite, spritelist, False,
                                                 pygame.sprite.collide_mask)

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

        elif sprite.velocity_y < 0:  # sprite top
            sprite.rect.top = platform.rect.bottom
            detectedcollisions["top"] = True

    # kill sprite if offscreen and is projectile
    if ((sprite.rect.left > WINDOW_WIDTH) or
       (sprite.rect.right < 0) or
       (sprite.rect.bottom < 0) or
       (sprite.rect.top > WINDOW_HEIGHT)):
        if isinstance(sprite, Projectile):
            sprite.kill()
        # check if 200 pixels below screen
        else:
            if sprite.rect.top > WINDOW_HEIGHT+200:
                # kill by deducting significant health
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


def distance(point1, point2):
    """Function that returns the distance between 2 points."""
    point1_x, point1_y = point1
    point2_x, point2_y = point2

    # use pythagoras to get distance between points
    dist = sqrt((point1_x - point2_x) ** 2 + (point1_y - point2_y) ** 2)

    return dist


# --------------- Constants --------------- #
PLATFORMLENGTH = 50
# automatically determine number of rows/columns
NUMBEROFCOLUMNS = int(WINDOW_WIDTH/PLATFORMLENGTH)
NUMBEROFROWS = int(WINDOW_HEIGHT/PLATFORMLENGTH)


class LevelMain(Screen):
    """Class for handling an individual game level's sprites and logic"""
    def __init__(self, screens, map_name):
        super().__init__(screens)

        # add screen specific event handlers to list of event handlers
        self.event_handlers.extend((self.handle_events_keyboard_down,
                                    self.handle_events_keyboard_up))

        # instantiate sprite groupd
        self.entities = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.finishpoints = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # load and render map sprites
        self.load_map(map_name)
        self.draw_map()

        self.update_cursor()

        # instantiate line to calculate collision between enemy projectile's
        # path and platform
        self.line = Line(self.player.rect.center, self.enemy.rect.center)

    def load_map(self, map_name):
        """Load level map as 2D array"""
        # 0 = nothing
        # 1 = platform
        # 2 = player spawn location
        # 3 map finish location
        self.gamemap = []

        # read the file with given map name
        with open("maps/" + map_name + ".txt", "r") as file:
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

        self.sprites.add(self.enemy, self.enemy.vision)
        self.entities.add(self.enemy)
        self.enemies.add(self.enemy)

        for row in range(NUMBEROFROWS):
            for col in range(NUMBEROFCOLUMNS):

                if self.gamemap[row][col] == 1:  # platforms
                    # colour, width, height, xpos, ypos
                    plat = Platform(RED, PLATFORMLENGTH, PLATFORMLENGTH,
                                    col*PLATFORMLENGTH, row*PLATFORMLENGTH)
                    self.sprites.add(plat)
                    self.platforms.add(plat)

                elif self.gamemap[row][col] == 2:  # player
                    self.player = Player(BLUE, 40, 70, col*PLATFORMLENGTH,
                                         row*PLATFORMLENGTH)
                    self.sprites.add(self.player, self.player.stats)
                    self.entities.add(self.player)

                elif self.gamemap[row][col] == 3:  # finish point
                    self.finishpoint = Platform(PINK, PLATFORMLENGTH,
                                                PLATFORMLENGTH,
                                                col*PLATFORMLENGTH,
                                                row*PLATFORMLENGTH)
                    self.sprites.add(self.finishpoint)
                    self.finishpoints.add(self.finishpoint)

    def move_player(self):
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

    def move_enemies(self):
        """Uses the move function to move each enemy sprite."""
        for enemy in self.enemies:
            collisions = move(enemy, self.platforms)
            if collisions["bottom"]:
                enemy.jumpmomentum = 0
                enemy.onplatform = True

            # if player top collides, momentum reset
            if collisions["top"]:
                enemy.jumpmomentum = 0
                enemy.onplatform = False

    def move_projectiles(self):
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
            collisions = list_groupcollisions(entity.projectiles,
                                              self.entities)
            # iterate through each item (key, value) in dictionary
            # key is projectile
            # value is list of entities that collided with projectile
            for projectile, entities_hit in collisions.items():
                # iterate through each entity hit by projectile
                for hit_entity in entities_hit:
                    # if hit entity is entity that fired the projectile, skip
                    if hit_entity == entity:
                        continue

                    projectile.kill()  # for each projectile (key), despawn it

                    # inflict projectile damage
                    hit_entity.hit(projectile.damage)
                    if entity == self.player:
                        self.player.score += 5

            self.sprites.add(entity.projectiles)

    def update_enemy_vision(self):
        """Check if the player is inside an enemy's vision, if so, let the
        Enemy object know."""
        # iterate through each enemy
        for enemy in self.enemies:
            enemy_radius = enemy.vision.radius
            enemy_center = enemy.rect.center

            # list of player points to check
            player_points = [self.player.rect.topleft,
                             self.player.rect.topright,
                             self.player.rect.bottomleft,
                             self.player.rect.bottomright]

            # iterate through each player point
            for player_point in player_points:
                # check if point within enemy radius
                if enemy_radius >= distance(enemy_center, player_point):
                    # line is used to model projectile's path
                    # method updates line's endpoints
                    self.line.update_location(enemy_center, player_point)

                    # check for collisions between line and platforms
                    # function returns list of collisions
                    collisions = list_collisions_mask(self.line,
                                                      self.platforms)

                    # if no collisions (i.e. collisions list is empty)
                    if not collisions:
                        # report sighting of player and update enemy with
                        # vector to player
                        enemy.spotted(True,
                                      vector(enemy_center, player_point, 10))
                        # end for loop early
                        break

            else:
                # report no sighting of player
                enemy.spotted(False)

    def list_platforms_beneath(self, sprite):
        """Method to return list of platforms directly under a sprite."""
        # move sprite down 1 pixel on screen
        sprite.rect.y += 1
        # carry out collision check between sprite and platforms
        collisionslist = list_collisions(sprite, self.platforms)
        # move sprite up 1 pixel to original position
        sprite.rect.y -= 1
        # return list of collisions
        return collisionslist

    def update_enemy_movement(self):
        """Update an enemy sprite's knowledge of platforms it is colliding
        with."""
        for enemy in self.enemies:
            # return list of platforms colliding with enemy
            collided_platforms = self.list_platforms_beneath(enemy)

            # if list not empty (i.e. there are platforms colliding with enemy)
            if collided_platforms:
                left_edge = None
                right_edge = None
                for platform in collided_platforms:
                    # locate left edge
                    if ((left_edge is None) or
                       (platform.rect.left < left_edge)):
                        left_edge = platform.rect.left
                    # locate right edge
                    if ((right_edge is None) or
                       (platform.rect.right > right_edge)):
                        right_edge = platform.rect.right

                # check if enemy at left edge
                if enemy.rect.left < left_edge:
                    # move in opposite direction
                    enemy.movingleft = False
                    enemy.movingright = True
                # check if enemy at right edge
                elif enemy.rect.right > right_edge:
                    # move in opposite direction
                    enemy.movingright = False
                    enemy.movingleft = True

    def check_finish(self):
        """Method to check if the level is finished (completed/failed).
        If player collides with finish points, level completed.
        If player dead attribute true, level failed."""
        if list_collisions(self.player, self.finishpoints) != []:
            self.selected = "level_complete"
        elif self.player.dead:
            self.selected = "level_fail"
        else:
            # level not finished, end function early
            return
        # level did finish, so confirm screen change
        self.confirmed = True

    def resume(self, pause_duration):
        """Method to properly resume the game after a game pause."""
        self.player.regulate_cooldown(pause_duration)

    def handle_events_keyboard_down(self, event):
        """Handle keyboard related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        # altf4 or window close button invokes pygame.QUIT
        if event.type == pygame.QUIT:
            self.terminate()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC: pause
                self.selected = "pause"
                self.confirmed = True
            elif event.key == pygame.K_x:  # X: end program
                self.terminate()
            elif event.key == pygame.K_LSHIFT:  # L Shift: sprint
                self.player.sprinting = True
            elif event.key == pygame.K_a:  # A: move left
                self.player.movingleft = True
            elif event.key == pygame.K_d:  # D: move right
                self.player.movingright = True
            elif event.key == pygame.K_w:  # W: jump
                self.player.jumping = True
            elif event.key == pygame.K_SPACE:  # Spacebar: shoot
                # generate velocity vector from player to cursor
                projectile_vector = vector(self.player.rect.center,
                                           self.cursor, 10)
                # spawn projectile with generated velocity
                self.player.fire(projectile_vector)
            elif event.key == pygame.K_h:
                self.player.hit(5)

            # enemy movement testing
            elif event.key == pygame.K_LEFT:  # left arrow
                self.enemy.movingleft = True
            elif event.key == pygame.K_RIGHT:  # right arrow
                self.enemy.movingright = True
            elif event.key == pygame.K_UP:  # up arrow
                self.enemy.jumping = True

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match

    def handle_events_keyboard_up(self, event):
        """Handle keyboard related events. If the given event matches, the
        corresponding actions for that matched event are carried out."""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:  # L Shift: stop sprint
                self.player.sprinting = False
            elif event.key == pygame.K_a:  # A: stop moving left
                self.player.movingleft = False
            elif event.key == pygame.K_d:  # D: stop moving right
                self.player.movingright = False
            elif event.key == pygame.K_w:  # W: stop jumping
                self.player.jumping = False

            # enemy movement testing
            elif event.key == pygame.K_LEFT:  # left arrow
                self.enemy.movingleft = False
            elif event.key == pygame.K_RIGHT:  # right arrow
                self.enemy.movingright = False
            elif event.key == pygame.K_UP:  # up arrow
                self.enemy.jumping = False

        # return to calling line if the event matched
        else:
            return False  # no match
        return True  # match

    def update(self):
        """Update the cursor and sprites and check if the game is finished."""
        self.update_cursor()

        self.handle_events()

        # call update method for each entity sprite
        self.entities.update()

        # move player, enemies and projectiles
        self.move_player()
        self.move_enemies()
        self.move_projectiles()

        # update enemies sight
        self.update_enemy_vision()

        # update enemy movement
        self.update_enemy_movement()

        # check for game finish
        self.check_finish()

        return self.process_next_screen()
