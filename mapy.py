# map.py
import random
import pygame

from tile import Tile

meandering = .15
spawn_rate = .01
river_size = 3
river_length = [50, 80]

class Map:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.num_rows = height // tile_size
        self.num_cols = width // tile_size
        self.tiles = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.generate_map()

    def generate_map(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.tiles[row][col] is None:
                    self.tiles[row][col] = Tile(col * self.tile_size, row * self.tile_size, self.tile_size, self.generate_tile_color(row, col))

    def generate_tile_color(self, row, col):
        if random.random() < spawn_rate:  # 1% chance for a river start
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                for c in range(col, min(col + random.randint(river_length[0], river_length[1]), self.num_cols)):
                    for r in range(row, min(row + river_size, self.num_rows)):
                        self.tiles[r][c] = Tile(c * self.tile_size, r * self.tile_size, self.tile_size, [58, 124, 242])
                        if random.random() < meandering and row - 1 >= 0:
                            row -= 1
                        elif random.random() < meandering and row + 1 < self.num_rows:
                            row += 1
                return [58, 124, 242]
            else:
                for r in range(row, min(row + random.randint(river_length[0], river_length[1]), self.num_rows)):
                    for c in range(col, min(col + river_size, self.num_cols)):
                        self.tiles[r][c] = Tile(c * self.tile_size, r * self.tile_size, self.tile_size, [58, 124, 242])
                        if random.random() < meandering and col - 1 >= 0:
                            col -= 1
                        elif random.random() < meandering and col + 1 < self.num_cols:
                            col += 1
                return [58, 124, 242]
        else:
            # Adjust the probabilities of selecting green and gold
            return random.choices([[121, 201, 35], [193, 199, 40]], weights=[0.7, 0.3])[0]  # Green with 70%, Gold with 30%

    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.tiles[row][col].draw(screen)
