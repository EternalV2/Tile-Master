import pygame
import random

from global_functions import *
from mapy import Map
from particle_emitter import Particle, ParticleEmitter
from obj import Obj

class MovingObject(Obj):
    def __init__(self, x, y, size, color, direction, team):

        anim_stack = []
        
        # NOTE DISABLED SPAWN ANIMATION
        anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_spawn4.png")
        anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_spawn3.png")
        anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_spawn2.png")
        anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_spawn1.png")

        img = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_spawn1.png"

        super().__init__(x, y, size, direction, 35*3, 15, img, anim_stack, True)
        
        self.color = color

        self.delete_time = 1

        self.team = team
        
        self.count = random.randint(0, 7)
        self.image_name = img

    def move(self, currmap):
        # Update the position only when the move counter reaches the move frequency        
        if self.anim_stack:
            time_now = pygame.time.get_ticks()
            
            if time_now < self.next_animation: 
                return

            self.next_animation = time_now + self.animation_time
            self.image_name = self.anim_stack.pop()
            return 

        if self.direction == 'lu':
            self.x -= 1
            self.y -= 1
        elif self.direction == 'ld':
            self.x -= 1
            self.y += 1
        elif self.direction == 'ru':
            self.x += 1
            self.y -= 1
        elif self.direction == 'rd':
            self.x += 1
            self.y += 1
        elif self.direction == 'r':
            self.x += 1
        elif self.direction == 'l':
            self.x -= 1
        elif self.direction == 'd':
            self.y += 1
        elif self.direction == 'u':
            self.y -= 1


        '''
        self.emitter.x = self.x
        self.emitter.y = self.y
        self.emitter.rect_x = self.x * TILE_SIZE
        self.emitter.rect_y = self.y * TILE_SIZE

        self.emitter.emit_particles()
        '''

        time_delta = checkTime(self.next_frame, self.frame_time)
        if time_delta ==-1:
            return
        else:
            self.next_frame = time_delta

        if self.count == 0:
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u0.png"
            self.count = 1
        elif self.count == 1: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u1.png"
            self.count = 2
        elif self.count == 2: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u2.png"
            self.count = 3
        elif self.count == 3: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u3.png"
            self.count = 4
        elif self.count == 4: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u4.png"
            self.count = 5
        elif self.count == 5: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u5.png"
            self.count = 6
        elif self.count == 6: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u6.png"
            self.count = 7
        elif self.count == 7: 
            self.image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_movement_2.0/fireball_u7.png"
            self.count = 0

        #self.image = pygame.transform.rotate(pygame.image.load(self.image_name), self.degrees)


        #self.rect.center = [self.x * TILE_SIZE, self.y * TILE_SIZE]

        # THIS IS FOR SELF DELETION
        if not inMap(self.x, self.y, self.direction, self.size):
            if self.delete_time == 1:
                self.delete_time = time_now = pygame.time.get_ticks() + 1500
            return -1

        else:
            return 1
