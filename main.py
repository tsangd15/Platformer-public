import pygame
from _settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GREEN

pygame.init()

resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("2D Platformer")

run = True

clock = pygame.time.Clock()

while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(GREEN)

    pygame.display.flip()

pygame.quit()
