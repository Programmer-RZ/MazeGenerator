import pygame, sys

from const import *
from algorithm import Backtracking
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

backtracking = Backtracking()
player = Player(backtracking.walls, backtracking.all_cells, backtracking.cells[0])

delay = 0

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))

    backtracking.draw(screen)

    if not backtracking.finished:
        backtracking.update()
    
    else:
        player.update()
        player.draw(screen)
    

    pygame.display.update()