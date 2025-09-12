import pygame

from mapy import Map
from global_functions import *
from collections import deque

class Brush():
    def __init__(self, x, y):
        self.size = 1
        self.x = x
        self.y = y 

        # USED FOR DRAWING STRAIGHT LINES
        self.mode = ""
        self.spec_x, self.spec_y = -1, -1

        # USED FOR LOADING THE IMAGES FOR THE BRUSH
        # NOTE GROUND AND GOLD ARE SPECIAL TILES WHICH NEED TO BE ADDED MANUALLY TO A LEVEL MAP FILE
        if TILE_SIZE == 10:
            # NOTE NEED TO DUPLICATE 10 PX TILES AND PUT THEM IN IMG / SPEC LIKE YOU DID FOR 16 PX GROUND AND GOLD TILES
            self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/ground_10.png")
            self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/ground_10.png"
        elif TILE_SIZE == 16: 
            self.image = pygame.image.load(f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/{MAP_NAME}/_16/ground_16.png")
            self.name = f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/{MAP_NAME}/_16/ground_16.png"

        # SIZE OF THE IMG OF THE TILE TO BE RENDERED (DEFAULT AT 10) AND WHETHER ITS WALKABLE
        self.img_tile_size = 10

        self.fill = False

    def update(self, x, y):
        self.x = x
        self.y = y
    
    # CAPPED AT A SIZE OF 13
    def resizeUp(self):
        self.size = min(self.size + 1, 13)
        #print(f"SIZE: {self.size}")

    def resizeDown(self):
        self.size = max(self.size - 1, 0)
        #print(f"SIZE: {self.size}")

    # NOTE DRAW EFFECTS ONLY SUPPORTS FREE DRAWS, NOT LINES
    # DRAW EFFECT IS A BOOL, NOT THE EFFECTS ARRAY
    # THE EFFECTS ARRAY IS FULL_MAP WHEN DRAW EFFECT IS TRUE
    def draw(self, undo_stack, full_map, draw_effects):
        #print(f"help: {self.x}, {self.y}, full_map[x][y]: {full_map[self.x][self.y]} brush.name: {self.name}")

        # TODO IMPLEMENT UNDO/REDO FOR EFFECTS
        if draw_effects: 
            # IF YOU ARE HERE, FULL_MAP IS THE EFFECTS MAP, WHICH IS WHY drawRectOneEffects
            # HANDELS THE ARRAY DIFFERENTLY THEN REGULAR drawRectOne.
            drawRectOne(self.x, self.y, self.size, self.image, self.name, full_map)
            #print(f"draw effects: {full_map}")

        elif self.mode == "":

            # TODO RIGHT NOW, CODE ONLY HANDLES UNDOING AND REDOING FOR FREE DRAWING, NOT LINES
            new_version_name_arr, new_version_img_arr = copyRect(self.x, self.y, self.size, full_map)
            new_version = UndoFrame(self.x, self.y, self.size, new_version_img_arr, new_version_name_arr)
            undo_stack.append(new_version)

            if not self.fill:
                drawRectOne(self.x, self.y, self.size, self.image, self.name, full_map)
            else:
                if 0 <= self.x < MAP_RC[1] and 0 <= self.y < MAP_RC[0]:
                    self.drawFill(self.x, self.y, self.name, self.image, full_map)

        elif self.mode == "line":
            if abs(self.spec_x - self.x) <= abs(self.spec_y - self.y): 
                drawRectOne(self.spec_x, self.y, self.size, self.image, self.name, full_map)

            else: 
                drawRectOne(self.x, self.spec_y, self.size, self.image, self.name, full_map)
        
    def colorPicker(self, x, y, full_map, sidebar):
        # IF YOU ARE DRAWING EFFECTS, POLL THE EFFECTS FIRST AND IF THE IMAGE DOES NOT EXIST, POLL THE MAP
        effects_found = False

        if full_map.transparent[x][y] != None: 
            if full_map.transparent[x][y].name != "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/transparent_10.png":
                self.image = pygame.image.load(full_map.transparent[x][y].name)
                self.name = full_map.transparent[x][y].name
                effects_found = True
                sidebar.draw_effects = True

        if not effects_found:
            self.image = full_map.tiles[x][y].image
            self.name = full_map.tiles[x][y].name
            sidebar.draw_effects = False
    
    def drawFill(self, x, y, new_image_name, new_image, full_map):

        old_image_name = full_map[x][y].name

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Initialize a queue for BFS
        queue = deque([(x, y)])

        seen = set()

        seen.add((x, y))

        # Perform the flood fill
        while queue:
            row, col = queue.popleft()
            
            # Replace the current image with the new image
            full_map[row][col].name = new_image_name
            full_map[row][col].image = new_image

            # Check all four directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                #print(f"sad: {0 <= new_row < MAP_RC[0] and 0 <= new_col < MAP_RC[1]}")
                #print(f"old img: {old_image_name}, new row: {new_row}, new col: {new_col}, curr: {full_map[new_row][new_col].name}")

                #print(f"2nd part: {full_map[new_row][new_col] == old_image_name}")
                print(f"RC- 1: {len(full_map)} 2: {len(full_map[0])}")

                #print(f"list {full_map[new_row][0].name}, new row: {new_row}")

                # If the new position is within bounds and matches the target image, add it to the queue
                if (0 <= new_row < len(full_map)) and (0 <= new_col < len(full_map[0])) and ((new_row, new_col) not in seen):
                    print(f"2.0000 list {full_map[new_row][0].name}, new row: {new_row}")
                    if (full_map[new_row][new_col].name == old_image_name):
                        queue.append((new_row, new_col))
                        seen.add((new_row, new_col))
        
# BASICALLY STRUCT (DATA STORAGE) FOR REDO'S & UNDO'S
class UndoFrame():
    def __init__(self, x, y, brush_size, img_arr, name_arr):
        self.x = x
        self.y = y
        self.brush_size = brush_size
        self.img_arr = img_arr
        self.name_arr = name_arr
