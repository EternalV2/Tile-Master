import pygame
from global_functions import *
import time
import math

# FUN CALCULATIONS AHEAD

class Camera:
    def __init__(self, center_obj):
        self.center_obj = center_obj

        # LEFT & RIGHT CAMERA SNAPPING POSITION
        self.camera_pos_x = [WIDTH / (TILE_SIZE * 2), ((MAP_SIZE[0] - (WIDTH / 2)) / TILE_SIZE)]

        # UP & DOWN CAMERA SNAPPING POSITION
        self.camera_pos_y = [HEIGHT / (TILE_SIZE * 2), ((MAP_SIZE[1] - (HEIGHT / 2)) / TILE_SIZE)]
        
        # FOR TILE_SIZE = 10PX, + .5 TO CAMERA_POS_X & CAMERA_POS_Y WORKS 
        #self.gimble_effect = [self.camera_pos_x[0] + .5, self.camera_pos_y[0] + .5]
        self.gimble_effect = [self.camera_pos_x[0] + .53, self.camera_pos_y[0] + .53]
        #self.gimble_effect = [self.camera_pos_x[0]+1, self.camera_pos_y[0]+1]

        self.prev_cursor_location = [None, None]
        self.prev_cursor_img = None

        # HANDLE ANCHOR POINTS (ANCHOR IS THE REFERENCE WE USE TO CONVERT BETWEEN RC (ROW-COL) and PX (PIXELS))
        # _________________________________________________________________________________________________________________________
        # UPPER LEFT
        if self.camera_pos_x[0] > SPAWN[0] and self.camera_pos_y[0] > SPAWN[1]:
            #print("1")
            self.anchor = [self.camera_pos_x[0] * TILE_SIZE, self.camera_pos_y[0] * TILE_SIZE]

        # BOTTOM RIGHT
        elif self.camera_pos_x[1] < SPAWN[0] and self.camera_pos_y[1] < SPAWN[1]:
            #print("2")
            self.anchor = [self.camera_pos_x[1] * TILE_SIZE, self.camera_pos_y[1] * TILE_SIZE]
        
        # UPPER RIGHT
        elif self.camera_pos_x[1] < SPAWN[0] and self.camera_pos_y[0] > SPAWN[1]:
            #print("3")
            self.anchor = [self.camera_pos_x[1] * TILE_SIZE, self.camera_pos_y[0] * TILE_SIZE]
            
        # BOTTOM LEFT
        elif self.camera_pos_x[0] > SPAWN[0] and self.camera_pos_y[1] < SPAWN[1]:
            #print(f"4")
            self.anchor = [self.camera_pos_x[0] * TILE_SIZE, self.camera_pos_y[1] * TILE_SIZE]

        # STRAIGHT RIGHT
        elif self.camera_pos_x[1] < SPAWN[0]:
            #print(f"5")
            self.anchor = [self.camera_pos_x[1] * TILE_SIZE, self.SPAWN[1] * TILE_SIZE]
            
        # STRAIGHT BOTTOM
        elif self.camera_pos_y[1] < SPAWN[1]:
            #print(f"6")
            self.anchor = [SPAWN[0] * TILE_SIZE, self.camera_pos_y[1] * TILE_SIZE]
            
        # STRAIGHT LEFT        
        elif self.camera_pos_x[0] > SPAWN[0]:
            #print("7")
            self.anchor = [self.camera_pos_x[0] * TILE_SIZE, SPAWN[1] * TILE_SIZE]

        # STRAIGHT UP
        elif self.camera_pos_y[0] > SPAWN[1]:
            #print("8")
            self.anchor = [SPAWN[0] * TILE_SIZE, self.camera_pos_y[0] * TILE_SIZE]

        else: 
            #print("9")
            self.anchor = [SPAWN[0] * TILE_SIZE, SPAWN[1] * TILE_SIZE]
        # _________________________________________________________________________________________________________________________


    def update(self, full_map):
        self.sprite_group = pygame.sprite.Group()
        self.map_sprite = pygame.sprite.Group()
        self.effects_sprite = pygame.sprite.Group()

        if self.center_obj.image != None:
            self.sprite_group.add(self.center_obj)

        '''
        print(f"POS X\t 0: {self.camera_pos_x[0]}, 1: {self.camera_pos_x[1]}")
        print(f"POS Y\t 0: {self.camera_pos_y[0]}, 1: {self.camera_pos_y[1]}")
        print(f"GIMBLE X: {self.gimble_effect[0]}, Y: {self.gimble_effect[1]}")
        '''

        # HANDLE CAMERA POSTION, PLAYER SPRITE POSITION, AND GIMBLE (TELLS US HOW FAR AWAY WE ARE FROM THE ANCHOR POINT)
        # _________________________________________________________________________________________________________________________

            
        # UPPER LEFT
        if self.camera_pos_x[0] > self.center_obj.x and self.camera_pos_y[0] > self.center_obj.y:
            #print("1")
            self.x = self.camera_pos_x[0] * TILE_SIZE
            self.y = self.camera_pos_y[0] * TILE_SIZE

            self.center_obj.rect.center = [(self.center_obj.x + 1) * TILE_SIZE, (self.center_obj.y + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)]

        # BOTTOM RIGHT
        elif self.camera_pos_x[1] < self.center_obj.x and self.camera_pos_y[1] < self.center_obj.y:
            #print(f"X: {(self.camera_pos_x[1] - (WIDTH / (2 * TILE_SIZE)))}")
            #print(f"Y: {(self.camera_pos_y[1] - (HEIGHT / (2 * TILE_SIZE)))}")
            #print("2")
            self.x = self.camera_pos_x[1] * TILE_SIZE
            self.y = self.camera_pos_y[1] * TILE_SIZE
            
            self.center_obj.rect.center = [(self.center_obj.x - (self.camera_pos_x[1] - (WIDTH / (2 * TILE_SIZE))) + 1) * TILE_SIZE, (self.center_obj.y - (self.camera_pos_y[1] - (HEIGHT / (2 * TILE_SIZE))) + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)]
        
        # UPPER RIGHT
        elif  self.camera_pos_x[1] < self.center_obj.x and self.camera_pos_y[0] > self.center_obj.y:
            #print("3")
            self.x = self.camera_pos_x[1] * TILE_SIZE
            self.y = self.camera_pos_y[0] * TILE_SIZE
            
            self.center_obj.rect.center = [(self.center_obj.x - (self.camera_pos_x[1] - (WIDTH / (2 * TILE_SIZE))) + 1) * TILE_SIZE, (self.center_obj.y + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)]

        # BOTTOM LEFT
        elif self.camera_pos_x[0] > self.center_obj.x and self.camera_pos_y[1] < self.center_obj.y:
            #print(f"4")
            self.x = self.camera_pos_x[0] * TILE_SIZE
            self.y = self.camera_pos_y[1] * TILE_SIZE
            
            self.center_obj.rect.center = [(self.center_obj.x + 1) * TILE_SIZE, (self.center_obj.y - (self.camera_pos_y[1] - (HEIGHT / (2 * TILE_SIZE))) + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)] 

        # STRAIGHT RIGHT
        elif self.camera_pos_x[1] < self.center_obj.x:
            #print(f"5")
            self.x = self.camera_pos_x[1] * TILE_SIZE
            self.y = self.center_obj.y * TILE_SIZE
            
            self.center_obj.rect.center = [(self.center_obj.x - (self.camera_pos_x[1] - (WIDTH / (2 * TILE_SIZE))) + 1) * TILE_SIZE, (self.camera_pos_y[0] + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - self.center_obj.rect.center[1]]

        # STRAIGHT BOTTOM
        elif self.camera_pos_y[1] < self.center_obj.y:
            #print(f"6")
            self.x = self.center_obj.x * TILE_SIZE
            self.y = self.camera_pos_y[1] * TILE_SIZE
            
            self.center_obj.rect.center = [(self.camera_pos_x[0] + 1) * TILE_SIZE, (self.center_obj.y - (self.camera_pos_y[1] - (HEIGHT / (2 * TILE_SIZE))) + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - self.center_obj.rect.center[0], self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)]        

        # STRAIGHT LEFT        
        elif self.camera_pos_x[0] > self.center_obj.x:
            #print("7")
            self.x = self.camera_pos_x[0] * TILE_SIZE
            self.y = self.center_obj.y * TILE_SIZE
            
            self.center_obj.rect.center = [(self.center_obj.x + 1) * TILE_SIZE, (self.camera_pos_y[0] + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - (self.gimble_effect[0] * TILE_SIZE), self.y - self.anchor[1] - self.center_obj.rect.center[1]] 

        # STRAIGHT UP
        elif self.camera_pos_y[0] > self.center_obj.y:
            #print("8")
            self.x = self.center_obj.x * TILE_SIZE
            self.y = self.camera_pos_y[0] * TILE_SIZE
            
            self.center_obj.rect.center = [(self.camera_pos_x[0] + 1) * TILE_SIZE, (self.center_obj.y + 1)* TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - self.center_obj.rect.center[0], self.y - self.anchor[1] - (self.gimble_effect[1] * TILE_SIZE)] 

        else: 
            #print("9")
            self.x = self.center_obj.x * TILE_SIZE
            self.y = self.center_obj.y * TILE_SIZE
            
            self.center_obj.rect.center = [(self.camera_pos_x[0] + 1) * TILE_SIZE, (self.camera_pos_y[0] + 1) * TILE_SIZE]
            self.gimble = [self.x - self.anchor[0] - self.center_obj.rect.center[0], self.y - self.anchor[1] - self.center_obj.rect.center[1]]

    def addE(self, obj, screen):

        obj.rect.center = [((obj.x * TILE_SIZE) - self.anchor[0] - self.gimble[0]), ((obj.y * TILE_SIZE) - self.anchor[1] - self.gimble[1])]

        self.sprite_group.add(obj)


    def addObj(self, obj, screen):

        obj.rect.center = [((obj.x * TILE_SIZE) - self.anchor[0] - self.gimble[0]), ((obj.y * TILE_SIZE) - self.anchor[1] - self.gimble[1])]

        obj.emitter.rect_x = obj.rect.center[0]
        obj.emitter.rect_y = obj.rect.center[1]
        obj.emitter.x = obj.x
        obj.emitter.y = obj.y

        obj.emitter.emit_particles()

        obj.emitter.update(self.anchor, self.gimble)

        obj.emitter.draw(screen, self)

        self.sprite_group.add(obj)

    def addMap(self, base, full_map):

        big = [self.y - (HEIGHT // (2 * TILE_SIZE)), self.y + (HEIGHT // (2 * TILE_SIZE))]
        boi = [self.x - (WIDTH // (2 * TILE_SIZE)), self.x + (WIDTH // (2 * TILE_SIZE))]

        global f
        global s, r

        for row in range(0, MAP_RC[1], 1):
            for col in range(0, MAP_RC[0], 1):
                if full_map.transparent[row][col] != None: 
                    full_map.transparent[row][col].rect.center = [(col * TILE_SIZE) - self.anchor[0] - self.gimble[0], (row * TILE_SIZE) - self.anchor[1] - self.gimble[1]]
                    self.effects_sprite.add(full_map.transparent[row][col])

                full_map.tiles[row][col].rect.center = [(col * TILE_SIZE) - self.anchor[0] - self.gimble[0], (row * TILE_SIZE) - self.anchor[1] - self.gimble[1]]
                    
                self.map_sprite.add(full_map.tiles[row][col])
    
    def renderMap(self, screen):
        screen.fill((255, 255, 255))
        self.map_sprite.update()
        self.map_sprite.draw(screen)
        self.map_sprite.empty()

        self.effects_sprite.update()
        self.effects_sprite.draw(screen)
        self.effects_sprite.empty()

    def renderObj(self, screen):
        self.sprite_group.update()
        self.sprite_group.draw(screen)
        self.sprite_group.empty()