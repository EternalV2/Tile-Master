import pygame
import os

from global_functions import *
from mapy import Map
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter
from camera import Camera 
from obj import Obj

class Player(Obj):
    def __init__(self, x, y, size, name, aim, speed, idle_movement, animation_time, playerFPS):

        anim_stack = []

        self.character = name
        self.image_name = IMG_DIR + self.character + '/' + 'u/0.png'
        self.frame_count = len(os.listdir(IMG_DIR + self.character + '/' + 'u/'))
        self.idle_movement = idle_movement
        
        super().__init__(x, y, size, "u", animation_time, playerFPS * 1.35, self.image_name, anim_stack, False)

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200

        self.next_wood = 1
        self.wood_cooldown = 500

        self.next_fireball = 1
        self.fireball_cooldown = 250
        self.fireball_direction = ""
        self.aim = aim

        self.inMotion = 0
        self.speed = speed

        self.walked = False

    # I THINK updateD HANDLES THE ANIMATION STACK
    def updateD(self, screen, map_tiles, moving_list):

        # CHECK TIME ______________________________________________________________________________________________________________
        time_delta = checkTime(self.next_animation, self.animation_time)
        if time_delta == -1:
            return
        else:
            self.next_animation = time_delta
        # ________________________________________________________________________________________________________________________

        img_dir = IMG_DIR + self.character + '/'

        player_row = self.x
        player_col = self.y
        
        # CAST FIREBALL ___________________________________________________________________________________________________________
        if self.inMotion:
            if not self.anim_stack:
                if self.direction == "ld" or self.direction == "lu" or self.direction == "l":
                    direction = "ld"
                elif self.direction == "rd" or self.direction == "ru" or self.direction == "r":
                    direction = "rd"
                elif self.direction == "d":
                    direction = "d"
                else: 
                    direction = "u"

                self.fireball_direction = self.direction

                pics = os.listdir(img_dir + 'casting/' + f"{direction}/")
                len_pics = len(pics)
                
                for i in range(len_pics-1, -1, -1):
                    self.anim_stack.append(img_dir + 'casting/' + f"{direction}/{i}.png")
            
            self.image_name = self.anim_stack.pop()
            self.image = pygame.image.load(self.image_name)

            if not self.anim_stack:
                self.inMotion = False

            # CHOOSE WHICH FRAME TO CAST THE FIREBALL AT
            # _________________________________________________________________________________________________________________________
            if self.direction == "d" or self.direction == "u":
                if self.anim_stack and self.anim_stack[-1][-5] == '4':
                    self.shoot(map_tiles, moving_list)
            
            else:
                if not self.anim_stack:
                    self.shoot(map_tiles, moving_list)
            # _________________________________________________________________________________________________________________________

        # _________________________________________________________________________________________________________________________

        # IDLE ____________________________________________________________________________________________________________________
        elif not self.anim_stack:
            #print(f"self.degrees: {self.degrees}")
            #print(f"self.direction: {self.direction}")
            curr_frame = (int(self.image_name[-5]) + 1) % self.frame_count

            if not self.walked:
                if not self.idle_movement:
                    curr_frame = 0

            if self.direction == "ld" or self.direction == "lu" or self.direction == "l":
                self.image_name = img_dir + 'ld/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)
            
            elif self.direction == "rd" or self.direction == "ru" or self.direction == "r":
                self.image_name = img_dir + 'rd/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)
                        
            elif self.direction == "d":
                self.image_name = img_dir + 'd/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)
            
            else:
                self.image_name = img_dir + 'u/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)

            self.walked = False
            self.inMotion = 0
        # _________________________________________________________________________________________________________________________

    def move(self, dx, dy, map_tiles):
        new_x = self.x + dx
        new_y = self.y + dy

        # Update direction based on movement
        if dx < 0 and dy < 0:
            self.direction = 'lu'
        elif dx < 0 and dy > 0:
            self.direction = 'ld'
        elif dx > 0 and dy < 0:
            self.direction = 'ru'
        elif dx > 0 and dy > 0:
            self.direction = 'rd'
        elif dx > 0:
            self.direction = 'r'
        elif dx < 0:
            self.direction = 'l'
        elif dy > 0:
            self.direction = 'd'
        elif dy < 0:
            self.direction = 'u'

        self.degrees = getDeg(self.direction)

        time_delta = checkTime(self.next_frame, self.frame_time)
        if time_delta == -1:
            return
        else:
            self.next_frame = time_delta

        #print(f"self.x {self.x} self.y {self.y}")
        if type(self.x) == float or type(self.y) == float:
            pass
            #print(f"hit")
        allow = inMap(self.x, self.y, self.direction, self.size)
        #print("MOVE???? ", allow)
        
        if allow and map_tiles[int(new_y // 1)][int(new_x // 1)].walkable:
            self.x = new_x
            self.y = new_y
        
        self.walked = True

    def shoot(self, map_tiles, moving_list):

        img_dir = IMG_DIR + self.character + '/'

        time_delta = checkTime(self.next_fireball, self.fireball_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_fireball = time_delta
        
        player_row = self.x
        player_col = self.y

        inBounds = inMap(self.x, self.y, self.direction, self.size)

        moving_list.append(MovingObject((self.x + self.aim[self.direction][0]), (self.y + self.aim[self.direction][1]), TILE_SIZE, [255, 0, 0], self.fireball_direction, "player"))