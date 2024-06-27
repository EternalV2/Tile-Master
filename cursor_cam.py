import pygame
from global_functions import *
import time
import math

# FUN CALCULATIONS AHEAD

class CursorCamera:

    def __init__(self, center_obj):
        self.x, self.y = 0, 0
        self.center_obj = center_obj
        self.sprite_group = pygame.sprite.Group()
        self.map_sprite = pygame.sprite.Group()

        self.wasd_pan = [0, 0]
        self.prev_img = None
        self.prev_name = None
        self.prev_num = [-1, -1]

        self.coord = [0, 0]
        self.show_sidebar = False


    def update(self, full_map, mouse_pos):
        # Calculate the current mouse position in tile coordinates
        mouse_x, mouse_y = mouse_pos
        mouse_x = (mouse_x // TILE_SIZE)
        mouse_y = (mouse_y // TILE_SIZE)

        # Update the center object position to follow the mouse
        self.center_obj.x = mouse_x
        self.center_obj.y = mouse_y
        
        self.x = self.center_obj.x * TILE_SIZE
        self.y = self.center_obj.y * TILE_SIZE
        
        self.center_obj.rect.center = [self.x, self.y]

        self.coord = [self.center_obj.x + self.wasd_pan[0], self.center_obj.y + self.wasd_pan[1]]
        #self.sprite_group.add(self.center_obj)

    def addMap(self, base, full_map, brush_size):

        cursorInMap = not 0 <= self.coord[0] < MAP_RC[0] or not 0 <= self.coord[1] < MAP_RC[1]

        for row in range(0, MAP_RC[1], 1):
            for col in range(0, MAP_RC[0], 1):

                '''
                if row == self.prev_num[0] and col == self.prev_num[1]:
                    full_map.tiles[row][col].image = self.prev_img
                    self.prev_num = [-1, -1]
                '''

                #??????????????????????

                #print(f"OBJ X: {self.center_obj.x} 0AN X: {self.wasd_pan[0]} RC[1] {MAP_RC[1]}")
                #print(f"OBJ Y: {self.center_obj.y} PAN Y: {self.wasd_pan[1]} RC[0] {MAP_RC[0]}")
            
                if cursorInMap:
                    self.prev_num = [0, 0]
                    #self.prev_img = full_map.tiles[row][col].image
                    self.prev_img = self.prev_name = None
                else: 
                    if row == self.coord[1] and col == self.coord[0]:
                        self.prev_num = [self.coord[1], self.coord[0]]
                        
                        #print(f"ROW: {row} PAN X: {self.wasd_pan[0]} RC[1] {MAP_RC[1]}")
                        #print(f"COL: {col} PAN Y: {self.wasd_pan[1]} RC[0] {MAP_RC[0]}")

                        #self.prev_img = full_map.tiles[row][col].image

                        self.prev_name, self.prev_img = copyRect(self.prev_num[0], self.prev_num[1], brush_size, full_map)                    

                        drawRectOne(row, col, brush_size, pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png"), "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png",full_map)
                
                full_map.tiles[row][col].rect.center = [(col * 10) - (self.wasd_pan[0] * 10), (row * 10) - (self.wasd_pan[1] * 10)]
                
                self.map_sprite.add(full_map.tiles[row][col])
    
    def renderMap(self, screen, full_map, brush_size):
        screen.fill((255, 255, 255))
        self.map_sprite.update()
        self.map_sprite.draw(screen)

        #full_map.tiles[self.prev_num[0]][self.prev_num[1]].image = self.prev_img
        drawRectArr(self.prev_num[0], self.prev_num[1], brush_size, self.prev_img, self.prev_name, full_map)

        self.prev_num = [-1, -1]
        self.prev_img = None
        self.prev_name = None

    def renderObj(self, screen):
        self.sprite_group.update()
        self.sprite_group.draw(screen)