import pygame
from global_functions import *
import time
import math
import sys
import random

# THIS DRAWS THE TILES THAT FOLLOW THE MOUSE 
# IT IS PROJECTED BY THE CAMERA AND COPY_RECT, PREV IMG, PREV NAME, AND PREV NUM  IS USED TO SAVE THE PREVIOUS STATE
# WHEN THE CAMERA MOVES, IT RELOADS THE PREVIOUS TILES

# FUN CALCULATIONS AHEAD

class CursorCamera:

    def __init__(self, center_obj):
        self.x, self.y = 0, 0
        self.center_obj = center_obj
        self.sprite_group = pygame.sprite.Group()

        self.map_sprite = pygame.sprite.Group()

        self.effects_sprite = pygame.sprite.Group()

        self.wasd_pan = [0, 0]
        self.prev_img = None
        self.prev_name = None
        self.prev_num = [-1, -1]

        self.coord = [0, 0]
        self.show_sidebar = False


    def update(self, mouse_pos):
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

    def addMap(self, full_map, brush_size):
        #tracemalloc.start()

        cursorNotInMap = not 0 <= self.coord[0] < MAP_RC[0] or not 0 <= self.coord[1] < MAP_RC[1]
        
        '''
        inits = tracemalloc.get_traced_memory()
        inits = [round(inits[0] / 1024 / 1024, 2), round(inits[1] / 1024 / 1024, 2)]
        '''
        
        #startTrackMalloc()
        #gc.set_debug(gc.DEBUG_LEAK)
        
        # ITERATE THROUGH BASEMAP, APPLY PANNING, ADD TO MAP_SPRITE GROUP, AND DRAW CURSOR HIGHLIGHT

        map_draw_start = pygame.time.get_ticks()

        for row in range(0, MAP_RC[1], 1):
            '''
            inits = tracemalloc.get_traced_memory()
            inits = [round(inits[0] / 1024 / 1024, 2), round(inits[1] / 1024 / 1024, 2)]
            '''
            for col in range(0, MAP_RC[0], 1):
                if cursorNotInMap:
                    self.prev_num = [0, 0]
                    #self.prev_img = full_map.tiles[row][col].image
                    self.prev_img = self.prev_name = None
                else: 
                    if row == self.coord[1] and col == self.coord[0]:
                        
                        # SAVE PREVIOUS STATE 
                        self.prev_num = [self.coord[1], self.coord[0]]
                        
                        self.prev_name = self.prev_img = None

                        self.prev_name, self.prev_img = copyRect(self.prev_num[0], self.prev_num[1], brush_size, full_map.tiles)                    
                        '''
                        nows = tracemalloc.get_traced_memory()
                        nows = [round(nows[0] / 1024 / 1024, 2), round(nows[1] / 1024 / 1024, 2)]
                        '''
                        # OVERWRITE TILES WITH CURSOR COLOR
                        # NOTE THIS "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/gold_10.png" NEEDS TO CHANGE BECAUSE THE GOLD 10 PX TILE SHOULD BE IN THE LEVEL_MAP FOLDER
                        drawRectOne(row, col, brush_size, pygame.image.load(f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/{MAP_NAME}/_{TILE_SIZE}/gold_{TILE_SIZE}.png"), "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/gold_10.png", full_map.tiles)

                        '''
                        nows_2 = tracemalloc.get_traced_memory()
                        nows_2 = [round(nows[0] / 1024 / 1024, 2), round(nows[1] / 1024 / 1024, 2)]
                        '''

                        '''                        
                        snapshot = tracemalloc.take_snapshot()
                        stats = snapshot.statistics('lineno')
                        print("Top 10 memory usage lines:")
                        for stat in stats[:10]:
                            print(stat)
                        '''

                        '''
                        if nows[0] != inits[0]:
                            print("inits:")
                            print(f"Current memory usage is {inits[0]} MB; Peak was {inits[1]} MB")

                            print(f"nows:")
                            print(f"Current memory usage is {nows[0]} MB; Peak was {nows[1]} MB")
                            exit()
                        else:
                            print("working")
                        '''

                # PANNING IS APPLIED HERE
                full_map.tiles[row][col].rect.center = [(col * TILE_SIZE) - (self.wasd_pan[0] * TILE_SIZE), (row * TILE_SIZE) - (self.wasd_pan[1] * TILE_SIZE)]
                self.map_sprite.add(full_map.tiles[row][col])

                start_row, end_row = max(0, self.coord[1] - brush_size + 1), min(MAP_RC[1], self.coord[1] + brush_size)
                start_col, end_col = max(0, self.coord[0] - brush_size + 1), min(MAP_RC[0], self.coord[0] + brush_size)

                if full_map.transparent[row][col] != None:

                    if cursorNotInMap or not ((start_row <= row < end_row) and (start_col <= col < end_col)):
                        full_map.transparent[row][col].rect.center = [(col * TILE_SIZE) - (self.wasd_pan[0] * TILE_SIZE), (row * TILE_SIZE) - (self.wasd_pan[1] * TILE_SIZE)]
                        self.effects_sprite.add(full_map.transparent[row][col])

            '''
            if row == 13:
                for bruh in full_map.tiles[random.randint(0, 104)]:
                    print("rough size 2.0x: ", full_map.tiles[random.randint(0, 104)])
            '''

        #endTrackMalloc()

        #tracemalloc.stop()
        '''
        map_draw_end = pygame.time.get_ticks()
        print()
        print("start")
        print(f"Map Draw took {map_draw_end - map_draw_start} ms with {len(full_map.tiles) * len(full_map.tiles[0])} tiles")
        
        effects_draw_start = pygame.time.get_ticks()

        # ITERATE THROUGH EFFECTS_MAP
        for effects_tile in full_map.transparent:

            # APPLY PANNING TO EFFECTS
            effects_tile.rect.center = [(effects_tile.y * TILE_SIZE) - (self.wasd_pan[0] * TILE_SIZE), (effects_tile.x * TILE_SIZE) - (self.wasd_pan[1] * TILE_SIZE)]

            # IF CURSOR IS NOT IN MAP, NO NEED TO OVERWRITE COLOR
            if cursorNotInMap: 
                self.effects_sprite.add(effects_tile)
            
            else:
                # MAKES SURE CURSOR COLOR IS APPLIED ON TOP OF EFFECTS
                # _________________________________________________________________________________________________________________________
                start_row, end_row = max(0, self.coord[1] - brush_size + 1), min(MAP_RC[1], self.coord[1] + brush_size)
                start_col, end_col = max(0, self.coord[0] - brush_size + 1), min(MAP_RC[0], self.coord[0] + brush_size)

                if not (start_row <= effects_tile.x < end_row and start_col <= effects_tile.y < end_col):
                    self.effects_sprite.add(effects_tile)
                # _________________________________________________________________________________________________________________________

        effects_draw_end = pygame.time.get_ticks()
        print(f"Effects Draw took {effects_draw_end - effects_draw_start} ms with {len(full_map.effects)} effects")
        print("end")
        print()
        '''

    def renderMap(self, full_map, screen, brush_size):
        screen.fill((255, 255, 255))
        self.map_sprite.update()
        self.map_sprite.draw(screen)

        self.effects_sprite.update()
        self.effects_sprite.draw(screen)

        self.map_sprite.empty()
        self.effects_sprite.empty()

        self.map_sprite = None
        self.effects_sprite = None

        self.map_sprite = pygame.sprite.Group()
        self.effects_sprite = pygame.sprite.Group()

        # THIS APPLIES THE PREVIOUS STATE TO THE MAP (STATE BEFORE IT WAS OVERWRITTEN BY CURSOR COLOR TILES)
        drawRectArr(self.prev_num[0], self.prev_num[1], brush_size, self.prev_img, self.prev_name, full_map.tiles)

        self.prev_num = [-1, -1]

        '''
        for i in range(len(self.prev_img)): 
            self.prev_img[i] = None
        for i in range(len(self.prev_name)):
            self.prev_name[i] = None
        '''
        
        self.prev_img = None
        self.prev_name = None

    def renderObj(self, screen):
        self.sprite_group.update()
        self.sprite_group.draw(screen)