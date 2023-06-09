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

        self.cell_size = CELL_SIZE
    
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
            cx *= self.cell_size
            cy *= self.cell_size

            west_line = []
            east_line = []
            south_line = []
            north_line = []

            if w:
                west_line = [(cx, cy), (cx, cy + self.cell_size)]
            
            if e:
                east_line = [(cx + self.cell_size, cy), (cx + self.cell_size, cy + self.cell_size)]
            
            if n:
                north_line = [(cx, cy), (cx + self.cell_size, cy)]
            
            if s:
                south_line = [(cx, cy + self.cell_size), (cx + self.cell_size, cy + self.cell_size)]
            
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
                    self.cell_size *= SCROLLING_SCALE
                    self.find_end()
            
            self.dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    def draw(self, screen, cx, cy):
            
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

            cell_x *= self.cell_size
            cell_y *= self.cell_size

            if cell_x + cx > -self.cell_size and cell_x + cx < WIDTH and cell_y + cy > -self.cell_size and cell_y + cy < HEIGHT:
                pygame.draw.rect(screen, color, (cell_x + cx, cell_y + cy, self.cell_size, self.cell_size))

            # draw walls
            w, e, n, s = self.walls[index]

            walls = self.calculate_wall(cell, w, e, n, s)

            west, east, north, south = walls

            if len(west) != 0:
                sx, sy = west[0]
                ex, ey = west[1]
                
                is_end_inbounds = (ex + cx > 0 and ex + cx < WIDTH and ey + cy > 0 and ey + cy < HEIGHT)
                is_start_inbounds = (sx + cx > 0 and sx + cx < WIDTH and sy + cy > 0 and sy + cy < HEIGHT)

                if is_end_inbounds or is_start_inbounds:
                    pygame.draw.line(screen, (255, 255, 255), (sx + cx, sy + cy), (ex + cx, ey + cy), 3)
            
            if len(east) != 0:
                sx, sy = east[0]
                ex, ey = east[1]

                is_end_inbounds = (ex + cx > 0 and ex + cx < WIDTH and ey + cy > 0 and ey + cy < HEIGHT)
                is_start_inbounds = (sx + cx > 0 and sx + cx < WIDTH and sy + cy > 0 and sy + cy < HEIGHT)

                if is_end_inbounds or is_start_inbounds:
                    pygame.draw.line(screen, (255, 255, 255), (sx + cx, sy + cy), (ex + cx, ey + cy), 3)
            
            if len(north) != 0:
                sx, sy = north[0]
                ex, ey = north[1]

                is_end_inbounds = (ex + cx > 0 and ex + cx < WIDTH and ey + cy > 0 and ey + cy < HEIGHT)
                is_start_inbounds = (sx + cx > 0 and sx + cx < WIDTH and sy + cy > 0 and sy + cy < HEIGHT)

                if is_end_inbounds or is_start_inbounds:
                    pygame.draw.line(screen, (255, 255, 255), (sx + cx, sy + cy), (ex + cx, ey + cy), 3)
            
            if len(south) != 0:
                sx, sy = south[0]
                ex, ey = south[1]
                
                is_end_inbounds = (ex + cx > 0 and ex + cx < WIDTH and ey + cy > 0 and ey + cy < HEIGHT)
                is_start_inbounds = (sx + cx > 0 and sx + cx < WIDTH and sy + cy > 0 and sy + cy < HEIGHT)

                if is_end_inbounds or is_start_inbounds:
                    pygame.draw.line(screen, (255, 255, 255), (sx + cx, sy + cy), (ex + cx, ey + cy), 3)
    