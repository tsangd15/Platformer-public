import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GREEN, RED
from _platform import Platform
from _player import Player

pygame.init()

resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("2D Platformer")

# setting variables
platformlength = 50

# automatically determine number of rows/columns
numberofcolumns = int(WINDOW_WIDTH/platformlength)
numberofrows = int(WINDOW_HEIGHT/platformlength)

# 0 = nothing
# 1 = platform
map = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ]

# Setting up sprite lists
sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Creating sprites then adding to sprite lists
player = Player(RED, 40, 70)
sprites.add(player)

for row in range(numberofrows):
    for col in range(numberofcolumns):

        if map[row][col] == 1:  # platforms
            plat = Platform(RED, platformlength, platformlength)
            plat.setlocation(col*platformlength, row*platformlength)
            sprites.add(plat)
            platforms.add(plat)


run = True

clock = pygame.time.Clock()

while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                run = False

        if event.type == pygame.KEYUP:
            pass

    screen.fill(GREEN)

    sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
