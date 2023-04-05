import pygame, sys

from const import *
from algorithm import Backtracking
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

backtracking = Backtracking()
player = Player(backtracking.walls, backtracking.all_cells, backtracking.cells[0])

camera_x, camera_y = 0, 0

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))

    backtracking.draw(screen, camera_x, camera_y)

    if not backtracking.finished:
        backtracking.update()
    
    else:
        player.cell_size = backtracking.cell_size

        player.update()

        camera_x = camera_x + (WIDTH / 2 - player.pos.x - camera_x) * 0.1;
        camera_y = camera_y + (HEIGHT / 2 - player.pos.y - camera_y) * 0.1;

        player.draw(screen, camera_x, camera_y)

    pygame.display.update()