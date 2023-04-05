import pygame

from const import *

class Player:
    def __init__(self, walls, cells, start):
        self.walls = walls
        self.cells = cells
        
        x, y = start

        self.width = 20
        self.height = 20

        self.pos = pygame.math.Vector2(
            (x - 1) * CELL_SIZE + CELL_SIZE / 2 - self.width / 2, 
            (y - 1) * CELL_SIZE + CELL_SIZE / 2 - self.height / 2)
        
        self.vel = pygame.math.Vector2(0, 0)
    
    def update(self):
        self.move()
        self.collision()

        self.pos += self.vel
    
    def move(self):
        keys = pygame.key.get_pressed()

        self.vel.x = 0
        self.vel.y = 0

        if keys[pygame.K_UP]:
            self.vel.y = -2
        
        if keys[pygame.K_DOWN]:
            self.vel.y = 2
        
        if keys[pygame.K_LEFT]:
            self.vel.x = -2
        
        if keys[pygame.K_RIGHT]:
            self.vel.x = 2
    
    def collision(self):
        future_x, future_y = self.pos.x + self.vel.x, self.pos.y + self.vel.y
        # find row and col of player
        row = int(future_x / CELL_SIZE) + 1
        col = int(future_y / CELL_SIZE) + 1

        neighbour_walls = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
            (row + 1, col + 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row - 1, col - 1),
            (row, col)
        ]

        for i in neighbour_walls:
            try:
                index = self.cells.index(i)
            except ValueError:
                continue

            wall = self.walls[index]
            x, y = self.cells[index]
            x -= 1
            y -= 1

            west, east, north, south = wall

            if west:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, 3, CELL_SIZE)
                if rect.colliderect(pygame.Rect(future_x, self.pos.y, self.width, self.height)):
                    self.vel.x = 0
                
                if rect.colliderect(pygame.Rect(self.pos.x, future_y, self.width, self.height)):
                    self.vel.y = 0
            
            if east:
                rect = pygame.Rect(x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE, 3, CELL_SIZE)
                if rect.colliderect(pygame.Rect(future_x, self.pos.y, self.width, self.height)):
                    self.vel.x = 0
                
                if rect.colliderect(pygame.Rect(self.pos.x, future_y, self.width, self.height)):
                    self.vel.y = 0
            
            if north:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, 3)
                if rect.colliderect(pygame.Rect(future_x, self.pos.y, self.width, self.height)):
                    self.vel.x = 0
                
                if rect.colliderect(pygame.Rect(self.pos.x, future_y, self.width, self.height)):
                    self.vel.y = 0
            
            if south:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE, CELL_SIZE, 3)
                if rect.colliderect(pygame.Rect(future_x, self.pos.y, self.width, self.height)):
                    self.vel.x = 0
                
                if rect.colliderect(pygame.Rect(self.pos.x, future_y, self.width, self.height)):
                    self.vel.y = 0
        
        # check if out of bounds
        
        if future_x >= WIDTH:
            self.vel.x
        
        if future_y >= HEIGHT:
            self.vel.y

    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.pos.x, 
                                               self.pos.y, 
                                               self.width, 
                                               self.height))