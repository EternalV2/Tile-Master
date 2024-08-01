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

# EFFECTS TAKE AROUND 2X AS LONG TO DRAW AS REG MAP TILES

class Map:
    def __init__(self, tile_size, map_size):
        self.tile_size = tile_size
        self.num_rows = map_size[1] // tile_size
        self.num_cols = map_size[0] // tile_size
        #print(f"BEFORE MAP: R: {self.num_rows} C: {self.num_cols}")
        self.tiles = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.transparent = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]

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

    '''
    def parseLine(self, input_string):

        parts = input_string.split(",")

        temp_x = int(parts[0])
        temp_y = int(parts[1])
        
        # NOTE NOTE NOTE
        #temp_size = int(parts[2])
        temp_size = 10

        temp_color = [int(parts[3].replace('[', '', 1)), int(parts[4]), int(parts[5].replace(']', '', 1))]
        temp_walkable = parts[6].strip() == 'True'
                            
        temp_name = parts[7].strip()
    '''


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

        #print(f"BETWEENES BEEK {len(string_array)}")

        for i in range(len(string_array)):

            load_transparent = False
            if i >= len(self.tiles):
                print(f"I IS NOW > SELF.TILES, SHOULD START TO ADD TO EFFECTS")
                load_transparent = True

            again = string_array[i].split('|')
            #print(f"\n\n\nFFF String: {string_array[i]}")
            #print(f"\n\n\nFFF Again: {again}")
            again.pop(0)
            again.pop(len(again) - 1)

            '''
            else:
                load_transparent_arr = string_array[i].split('|')
                #self.loadEffects(load_transparent_arr)
                return
            '''

            #print(f"\n\n\n\n\n\n\nAGAIN: {again}\n\n\n\n\n\n\n")
            j_tile_ptr = -1

            # CONSTRUCTION
            # _________________________________________________________________________________________________________________________
            '''
            print()
            print(f"START")
            print(f"I:")
            print(f"len string arr: {len(string_array)}")
            
            print(f"J:")
            print(f"len again: {len(again)}")

            print(f"Len Map.tiles: {len(self.tiles)}")
            print(f"Len Map.tiles[0]: {len(self.tiles[0])}")
            print(f"END")
            '''
            # _________________________________________________________________________________________________________________________

            #print(f"LE: {load_transparent}")

            for j in range(len(again)):

                if again[j] == "None":
                    j_tile_ptr += 1
                    #print(f"I: {i}, J: {j_tile_ptr}, LEN: {len(self.tiles)}")
                    self.transparent[i % len(self.tiles)][j_tile_ptr] = None

                elif again[j] != ",":
                    j_tile_ptr += 1

                    if j_tile_ptr >= len(self.tiles[0]):
                        #print("J_TILE_PTR STOPPED")
                        continue
                    else:
                        pass

                    input_string = again[j]
                    parts = input_string.split(",")

                    temp_x = int(parts[0])
                    temp_y = int(parts[1])
                    
                    # NOTE NOTE NOTE
                    #temp_size = int(parts[2])
                    temp_size = 10

                    temp_color = [int(parts[3].replace('[', '', 1)), int(parts[4]), int(parts[5].replace(']', '', 1))]
                    temp_walkable = parts[6].strip() == 'True'
                                        
                    temp_name = parts[7].strip()

                    temp_tile = Tile(temp_x, temp_y, temp_size, [0,0,0], temp_name, temp_walkable)

                    if i >= len(self.tiles) and i != len(string_array) - 1:
                        #print(f"BREAK I: {i}")
                        pass
                        #exit()

                    if j_tile_ptr >= len(self.tiles[0]) and i != len(string_array) - 1:
                        #print(f"BREAK J: {j_tile_ptr}")
                        pass
                        #exit()

                    if load_transparent:
                        self.transparent[i % len(self.tiles)][j_tile_ptr] = temp_tile
                    else:
                        self.tiles[i][j_tile_ptr] = temp_tile

                    '''
                    if j_tile_ptr == len(again) - 1:
                        print("error in map load")
                        exit()
                    '''

    def loadEffects(self, input_string):
        input_string.pop(0)
        input_string.pop(-1)
        for i in range(len(input_string)):
            j_tile_ptr = -1
            if input_string[i] != ",":
                j_tile_ptr += 1
                #print(f"I: {i}, {input_string[i]}")
                parts = input_string[i].split(",")
                temp_x = int(parts[0])
                temp_y = int(parts[1])
                
                # NOTE NOTE NOTE
                #temp_size = int(parts[2])
                temp_size = 10

                temp_color = [int(parts[3].replace('[', '', 1)), int(parts[4]), int(parts[5].replace(']', '', 1))]
                temp_walkable = parts[6].strip() == 'True'
                                    
                temp_name = parts[7].strip()

                temp_tile = Tile(temp_x, temp_y, temp_size, [0,0,0], temp_name, temp_walkable)
                self.tiles[i][j_tile_ptr] = temp_tile

    def copy(self, tile_size, map_size):
        print("LLLL")
        new_version = Map(tile_size, map_size)
        print(f"SDA {map_size[1] // tile_size}")
        for row in range(len(self.tiles)):
            for col in range(map_size[0] // tile_size):
                new_version.tiles[row][col] = self.tiles[row][col].copy()
        return new_version

    def sortEffects(self):
        print()
        print("In sorted")
        sorted_effects_x = sorted(self.effects, key = lambda Tile: Tile.x)
        sorted_effects_y = sorted(self.effects, key = lambda Tile: Tile.y)
        
        print(f"In sorted x")
        
        for i in range(len(sorted_effects_x)):
            print(f"X: {sorted_effects_x[i].x}, Y: {sorted_effects_x[i].y}")
        
        print(f"In sorted x")
        for i in range(len(sorted_effects_y)):
            print(f"X: {sorted_effects_x[i].x}, Y: {sorted_effects_x[i].y}")

        seen_set = set()

        unique_tiles = []

        for tile in reversed(self.effects):
            coords = (tile.x, tile.y)
            if coords not in seen_set:
                seen_set.add((coords))
                unique_tiles.append(tile)
        
        unique_tiles.reverse()

        print(f"unique_tiles")
        for i in range(len(unique_tiles)):
            print(f"X: {unique_tiles[i].x}, Y: {unique_tiles[i].y}")

        self.effects = unique_tiles

        print(f"Done")
        print()