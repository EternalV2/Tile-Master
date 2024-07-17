# map.py
import random
import pygame
import os

from tile import Tile
from global_functions import *

meandering = .15
spawn_rate = .00
river_size = 3
river_length = [1750, 100]

class Map:
    def __init__(self, tile_size, map_size):
        self.tile_size = tile_size
        self.num_rows = map_size[1] // tile_size
        self.num_cols = map_size[0] // tile_size
        #print(f"BEFORE MAP: R: {self.num_rows} C: {self.num_cols}")
        self.tiles = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.tiles[row][col] = Tile(col * self.tile_size, row * self.tile_size, self.tile_size, [0,0,0], "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png", False)
        
        #print(f"AFTER MAP: R: {len(self.tiles)} C: {len(self.tiles[0])}")

        #self.generate_map()

    def generate_map(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.tiles[row][col] is None:
                    self.tiles[row][col] = Tile(col * self.tile_size, row * self.tile_size, self.tile_size, self.generate_tile_color(row, col), "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png", False)

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
    
    # WHAT THIS DOES IS OVERWRITE THE CURRENT MAP
    # PROBS NOT SUPER EFFICENT :)

    #????????????????? 
    def load(self, path):
        
        with open(path, 'r') as file: 
            result_string = file.read()

        #string_array = [line.split(',') for line in result_string.split('\n')]

        string_array = result_string.split('\n')

        #print("HOLD HOLD")
        #print(string_array[0])

        for i in range(len(string_array)):
            again = string_array[i].split('|')
            again.pop(0)
            again.pop(len(again) - 1)
            
            #print(f"\n\n\n\n\n\n\nAGAIN: {again}\n\n\n\n\n\n\n")
            j_tile_ptr = -1
            for j in range(len(again)):
                #print(f"AGAIN: {agaçin}")
                if again[j] != ",":
                    j_tile_ptr += 1
                    input_string = again[j]
                    parts = input_string.split(",")

                    #print(f"I: {i}, J: {j}, PARTS: {parts}")

                    temp_x = int(parts[0])
                    temp_y = int(parts[1])
                    temp_size = int(parts[2])
                    temp_color = [int(parts[3].replace('[', '', 1)), int(parts[4]), int(parts[5].replace(']', '', 1))]
                    temp_walkable = parts[6].strip() == 'True'
                    
                    #print(f"Parts 6: {parts[6]}, temp walkable: {temp_walkable}")
                    
                    temp_name = parts[7].strip()


                    #print(f"X: {temp_x} Y: {temp_y} SIZE: {temp_size} COLOR: {temp_color} WALKABLE: {temp_walkable} NAME: {temp_name}")
                    #print(f"\n\n\n\n\n\nI: {i}, J: {j}, LEN ROW: {len(string_array)}, LEN COL: {len(again)}")
                    temp_tile = Tile(temp_x, temp_y, temp_size, [0,0,0], temp_name, temp_walkable)
                    temp_tile.image = pygame.image.load(temp_tile.name)
                    #print(f"WOAH {temp_tile.name}")

                    self.tiles[i][j_tile_ptr] = temp_tile

                    if j_tile_ptr == len(again) - 1:
                        print("error in map load")
                        exit()
                    #print(f"I: {i}, J TILE PTR: {j_tile_ptr}")

    def copy(self, tile_size, map_size):
        print("LLLL")
        new_version = Map(tile_size, map_size)
        print(f"SDA {map_size[1] // tile_size}")
        for row in range(len(self.tiles)):
            for col in range(map_size[0] // tile_size):
                new_version.tiles[row][col] = self.tiles[row][col].copy()
        return new_version
