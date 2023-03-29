import pygame, sys

from const import *
from algorithm import Backtracking

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

backtracking = Backtracking()

delay = 0

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))

    if delay % 5 == 0:
        backtracking.update()

    backtracking.draw(screen)

    delay += 1

    pygame.display.update()