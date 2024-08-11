"""Main game file"""
import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GREEN, RED, BLUE
from _platform import Platform
from _player import Player

pygame.init()

resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("2D Platformer")

# setting variables
PLATFORMLENGTH = 50

# automatically determine number of rows/columns
NUMBEROFCOLUMNS = int(WINDOW_WIDTH/PLATFORMLENGTH)
NUMBEROFROWS = int(WINDOW_HEIGHT/PLATFORMLENGTH)

# 0 = nothing
# 1 = platform
gamemap = [
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
  [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ]

# Setting up sprite lists
sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Creating sprites then adding to sprite lists
player = Player(BLUE, 40, 70)
sprites.add(player)

for row in range(NUMBEROFROWS):
    for col in range(NUMBEROFCOLUMNS):

        if gamemap[row][col] == 1:  # platforms
            plat = Platform(RED, PLATFORMLENGTH, PLATFORMLENGTH)
            plat.setlocation(col*PLATFORMLENGTH, row*PLATFORMLENGTH)
            sprites.add(plat)
            platforms.add(plat)

# collision functions


def list_collisions(sprite, spritelist):
    """Takes in a singular sprite and spritelist
    Returns list of sprites in spritelist that collide with singular sprite"""
    collisionslist = pygame.sprite.spritecollide(sprite, spritelist, False)
    return collisionslist


def move(sprite, platformlist):
    """Function to move specific sprite, taking into account collisions with
    sprites under the provided spritelist.

    Function moves the sprite in the x direction first, then corrects it's
    location if it has collided, then moves the sprite in the y direction and
    corrects if it has collided. Returns the sides it has collided with for
    further conditional actions."""
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

    return detectedcollisions


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
                player.movingleft = True
            if event.key == pygame.K_d:
                player.movingright = True
            if event.key == pygame.K_w:
                player.jumping = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.movingleft = False
            if event.key == pygame.K_d:
                player.movingright = False
            if event.key == pygame.K_w:
                player.jumping = False

    # --------------- game logic ------------- #

    # call update function for each sprite in sprites list
    sprites.update()

    # secondary keybind detection for holding key
    keys = pygame.key.get_pressed()

    # move player
    collisions = move(player, platforms)
    if collisions["bottom"]:
        player.jumpmomentum = 0
        player.airduration = 0
    else:
        player.airduration += 1

    # if player top collides, momentum reset
    if collisions["top"]:
        player.jumpmomentum = 0

    screen.fill(GREEN)

    sprites.draw(screen)

    # update the screen
    pygame.display.flip()

pygame.quit()
