import pygame

from mapy import Map
from global_functions import *

class Brush():
    def __init__(self, x, y):
        self.size = 1
        self.x = x
        self.y = y 

        # USED FOR DRAWING STRAIGHT LINES
        self.mode = ""
        self.spec_x, self.spec_y = -1, -1

        # USED FOR LOADING THE IMAGES FOR THE BRUSH
        self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/ground_10.png")
        self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/ground_10.png"

        # SIZE OF THE IMG OF THE TILE TO BE RENDERED (DEFAULT AT 10) AND WHETHER ITS WALKABLE
        self.img_tile_size = 10

    def update(self, x, y):
        self.x = x
        self.y = y
    
    # CAPPED AT A SIZE OF 13
    def resizeUp(self):
        self.size = min(self.size + 1, 13)
        print(f"SIZE: {self.size}")

    def resizeDown(self):
        self.size = max(self.size - 1, 0)
        print(f"SIZE: {self.size}")

    def draw(self, undo_stack, full_map):

        if self.mode == "":

            # TODO RIGHT NOW, CODE ONLY HANDLES UNDOING AND REDOING FOR FREE DRAWING, NOT LINES
            new_version_name_arr, new_version_img_arr = copyRect(self.x, self.y, self.size, full_map)
            new_version = UndoFrame(self.x, self.y, self.size, new_version_img_arr, new_version_name_arr)
            undo_stack.append(new_version)

            drawRectOne(self.x, self.y, self.size, self.image, self.name, full_map)
            

        elif self.mode == "line":
            if abs(self.spec_x - self.x) <= abs(self.spec_y - self.y): 
                drawRectOne(self.spec_x, self.y, self.size, self.image, self.name, full_map)

            else: 
                drawRectOne(self.x, self.spec_y, self.size, self.image, self.name, full_map)

    def colorPicker(self, x, y, full_map):
        self.image = full_map.tiles[x][y].image
        self.name = full_map.tiles[x][y].name

# BASICALLY STRUCT (DATA STORAGE) FOR REDO'S & UNDO'S
class UndoFrame():
    def __init__(self, x, y, brush_size, img_arr, name_arr):
        self.x = x
        self.y = y
        self.brush_size = brush_size
        self.img_arr = img_arr
        self.name_arr = name_arr
