import pygame
from random import choice, randint
from math import sqrt, pow

from const import *

class Backtracking:
    def __init__(self):
        rx, ry = randint(1, COL), randint(1, ROW)

        self.cells = [(rx, ry)]
        self.all_cells = [(rx, ry)]
        self.walls = [(True, True, True, True)]
        #           North    South     West    East
        self.dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        self.finished = False;
    
        self.dead_ends = []
        self.end = (-1, -1)
    
    def find_end(self):
        longest_dist = 0
        sx, sy = self.cells[0]
        for end in self.dead_ends:
            ex, ey = end

            # sqrt((x2 - x1)^2 + (y2 - y1)^2)
            dist = sqrt(pow((sx - ex), 2) + pow((sy - ey), 2))

            if abs(dist) > longest_dist:
                longest_dist = dist
                self.end = (ex, ey)
            
    
    def calculate_wall(self, cell, w, e, n, s):
            cx, cy = cell
            cx -= 1
            cy -= 1
            cx *= CELL_SIZE
            cy *= CELL_SIZE

            west_line = []
            east_line = []
            south_line = []
            north_line = []

            if w:
                west_line = [(cx, cy), (cx, cy + CELL_SIZE)]
            
            if e:
                east_line = [(cx + CELL_SIZE, cy), (cx + CELL_SIZE, cy + CELL_SIZE)]
            
            if n:
                north_line = [(cx, cy), (cx + CELL_SIZE, cy)]
            
            if s:
                south_line = [(cx, cy + CELL_SIZE), (cx + CELL_SIZE, cy + CELL_SIZE)]
            
            return (west_line, east_line, north_line, south_line)

    
    def remove_walls(self, cell1, cell2):
        cell1_index = self.all_cells.index(cell1)
        cell2_index = self.all_cells.index(cell2)

        c1_w, c1_e, c1_n, c1_s = self.walls[cell1_index]
        c2_w, c2_e, c2_n, c2_s = self.walls[cell2_index]

        cell1_walls = self.calculate_wall(cell1, c1_w, c1_e, c1_n, c1_s)
        cell2_walls = self.calculate_wall(cell2, c2_w, c2_e, c2_n, c2_s)

        c1_west, c1_east, c1_north, c1_south = cell1_walls
        c2_west, c2_east, c2_north, c2_south = cell2_walls

        if c1_west == c2_east:
            c1_w = False
            c2_e = False
        
        if c1_east == c2_west:
            c1_e = False
            c2_w = False
        
        if c1_north == c2_south:
            c1_n = False
            c2_s = False
        
        if c1_south == c2_north:
            c1_s = False
            c2_n = False
        
        self.walls[cell1_index] = (c1_w, c1_e, c1_n, c1_s)
        self.walls[cell2_index] = (c2_w, c2_e, c2_n, c2_s)
    
    def update(self):
        if len(self.cells) != 0:
            x, y = self.cells[-1]

            for _ in range(len(self.dir)):
                dx, dy = choice(self.dir)

                neighbour_x, neighbour_y = x + dx, y + dy

                in_grid = (neighbour_x >= 1 and neighbour_x <= COL and neighbour_y >= 1 and neighbour_y <= ROW)
                is_neighbour = ((neighbour_x, neighbour_y) not in self.all_cells)

                if in_grid and is_neighbour:
                    self.all_cells.append((neighbour_x, neighbour_y))
                    self.walls.append((True, True, True, True))

                    # remove walls
                    self.remove_walls(self.cells[-1], self.all_cells[-1])
                    self.remove_walls(self.all_cells[-2], self.all_cells[-1])

                    self.cells.append((neighbour_x, neighbour_y))
                    break

                else:
                    self.dir.remove((dx, dy));

            if len(self.dir) == 0:
                # backtrack, but don't remove the last cell, it will be the green square
                if len(self.cells) > 1:
                    self.dead_ends.append(self.cells[-1])
                    self.cells.remove(self.cells[-1])
                
                else:
                    self.finished = True
                    self.find_end()
            
            self.dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    def draw(self, screen):
            
        for index, cell in enumerate(self.all_cells):
            # draw cell, if cell is green square, draw green square
            # if cell is end cell, draw end cell
            color = (0, 0, 0)
            if cell == self.cells[-1]:
                color = (0, 255, 0)
            
            elif cell == self.end:
                color = (255, 0, 0)
            else:
                color = (60, 60, 60)

            cell_x, cell_y = cell
            cell_x -= 1
            cell_y -= 1

            pygame.draw.rect(screen, color, (cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # draw walls
            w, e, n, s = self.walls[index]

            walls = self.calculate_wall(cell, w, e, n, s)

            west, east, north, south = walls

            if len(west) != 0:
                pygame.draw.line(screen, (255, 255, 255), west[0], west[1], 3)
            
            if len(east) != 0:
                pygame.draw.line(screen, (255, 255, 255), east[0], east[1], 3)
            
            if len(north) != 0:
                pygame.draw.line(screen, (255, 255, 255), north[0], north[1], 3)
            
            if len(south) != 0:
                pygame.draw.line(screen, (255, 255, 255), south[0], south[1], 3)
    