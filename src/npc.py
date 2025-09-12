import pygame
import random
import os

from global_functions import *
from mapy import Map
from tile import Tile
from player import Player
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter
from obj import Obj

# NOTE ALOT OF REUSED CODE BETWEEN PLAYER.PY and NPC.PY
# TODO MAKE A CHARACTER CLASS WHICH INHERITS THE OBJ CLASS AND WHICH NPC AND PLAYER INHERIT

class Npc(Obj):
    # X AND Y ARE RC COORDINATES, NOT PX
    def __init__(self, x, y, size, team, name, aim, speed, idle_movement, enemyFPS):
        
        self.character = name
        self.image_name = IMG_DIR + self.character + '/' + "u/0.png"
        self.frame_count = len(os.listdir(IMG_DIR + self.character + '/' + 'u/'))
        self.idle_movement = idle_movement

        anim_stack = []

        super().__init__(x, y, size, "u", enemyFPS * 2, enemyFPS * 1.35, self.image_name, anim_stack, False)

        # PX FOR INTERNAL USE ONLY        
        self.px_x = x * TILE_SIZE
        self.px_y = y * TILE_SIZE

        self.last_direction = "u"

        self.next_fireball = 1
        self.fireball_cooldown = 600
        self.aim = aim

        self.inMotion = 0

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200
        
        self.speed = speed
        
        self.team = team
        self.walked = False
        
    def updateD(self, moving_list):

        # CHECK TIME ______________________________________________________________________________________________________________
        time_delta = checkTime(self.next_animation, self.animation_time)
        if time_delta == -1:
            return
        else:
            self.next_animation = time_delta
        # ________________________________________________________________________________________________________________________

        # IDLE ____________________________________________________________________________________________________________________
        if not self.anim_stack:
            curr_frame = (int(self.image_name[-5]) + 1) % self.frame_count
            img_dir = IMG_DIR + self.character + '/'

            if not self.walked:
                if not self.idle_movement:
                    curr_frame = 0

            if self.last_direction == "ld" or self.last_direction == "lu" or self.last_direction == "l":
                self.image_name = img_dir + 'ld/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)

            elif self.last_direction == "rd" or self.last_direction == "ru" or self.last_direction == "r":
                self.image_name = img_dir + 'rd/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)

            elif self.last_direction == "u":
                self.image_name = img_dir + 'u/' + f"{curr_frame}.png"
                self.image = pygame.image.load(self.image_name)
            
            elif self.last_direction == "d":
                self.image_name = img_dir + 'd/' + f"{curr_frame}.png"
                #print(f"ddd")
                #print(f"self.image_name: {self.image_name}")
                self.image = pygame.image.load(self.image_name)

            self.walked = False
            self.inMotion = 0
        # _________________________________________________________________________________________________________________________

        # CAST FIREBALL ___________________________________________________________________________________________________________
        else:
            if len(self.last_direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load(self.anim_stack.pop()), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load(self.anim_stack.pop()), self.degrees)

            self.inMotion = 1
        # _________________________________________________________________________________________________________________________


    def move(self, player, moving_list, all_enemies, map_tiles):

        # print("START")
        # print()

        # CHECK THAT THE ENEMY IS FOLLOWING HIS FPS
        # _________________________________________________________________________________________________________________________
        time_delta = checkTime(self.next_frame, self.frame_time)
        if time_delta == -1:
            return
        else:
            self.next_frame = time_delta
        # _________________________________________________________________________________________________________________________

        # IMPLEMENT RANDOM MOTION & MAKE SURE IT IS IN THE MAP
        # VERY OUTDATED, NEEDS OVERHAULL !!!
        # _________________________________________________________________________________________________________________________
        rand_move = 0

        #print(f"x: {self.px_x}, y: {self.px_y}")
        #print(f"map len: {len(map_tiles)}, map[x][y]: {map_tiles[self.px_y][self.px_x-1].color != [58, 124, 242]}")
        '''
        if random.random() > 0:
            #print(f"crash incoming")
            if basicBounds([self.x - 1, self.y]) and map_tiles[int(self.y // 1)][int((self.x - 1) // 1)].walkable:
                self.x -= 1
                return
    
        if random.random() > .99:
            rand_move = self.px_x + 1
            if basicBounds([self.x + 1, self.y]) and map_tiles[int(self.y // 1)][int((self.x + 1) // 1)].walkable:
                self.x += 1
                return

        if random.random() > .99:
            if basicBounds([self.x, self.y + 1]) and map_tiles[int((self.y + 1) // 1)][int(self.x // 1)].walkable:
                self.y += 1
                return

        if random.random() > .99:
            if basicBounds([self.x, self.y - 1]) and map_tiles[int((self.y - 1) // 1)][int((self.x) // 1)].walkable:
                self.y -= 1
                return
        '''
        # _________________________________________________________________________________________________________________________

        # CALCULATE THE VECTOR, DISTANCE, AND NORMALIZED VECTOR FROM THE ENEMEY TO THE PLAYER,
        # WE USE THE ORIGINAL VECTOR TO CALCULATE THE DIRECTION AND LAST_DIRECITON OF THE PLAYER LATER. 
        # _________________________________________________________________________________________________________________________
        direction_vector_ori = calcVector([player.x, player.y], [self.x, self.y])
        distance = calcDist(direction_vector_ori)
        direction_vector = norm(direction_vector_ori)

        # print(f"DIR X: {direction_vector[0]} DIR Y: {direction_vector[1]}")

        if distance == 0:
            return
        # _________________________________________________________________________________________________________________________

        # EXTRACT THE HORIZONTAL AND VERTICAL COMPONENTS AND SEE IF THE ENEMY IS WITHIN ATTACKING RANGE OR IF THE ENEMY SHOULD STOP MOVING TOWARDS THE PLAYER
        # _________________________________________________________________________________________________________________________
        horizontal_component = direction_vector[0]
        vertical_component = direction_vector[1]

        in_range = 0
        close_enough = 0

        if distance < 25:
            in_range = 1
            #print(f"range")
            if distance < 10:
                close_enough = 1
                #print(f"close")
            else:
                close_enough = 0 
        else: 
            in_range = 0
            close_enough = 0 
        # _________________________________________________________________________________________________________________________

        # CALCULATE THE SEPERATION VECTOR OF OTHER ENEMIES TO MAKE SURE THEY DONT GROUP UP ON THE SAME TILE AND TYHE APPLY THE SEPERATION FORCE
        # _________________________________________________________________________________________________________________________

        separation_vector = [0, 0]
        close = [float('inf'), float('inf')]

        for enemy in all_enemies:
            if enemy != self:
                '''
                curr_vector = calcVector([enemy.x, enemy.y], [self.x, self.y])
                distance_to_enemy = calcDist(curr_vector)

                separation_distance = 70

                if distance_to_enemy < separation_distance:
                    separation_vector[0] += self.x + enemy.x
                    separation_vector[1] += self.y + enemy.y
                '''
            
                if abs(self.x - enemy.x) < abs(self.x - close[0]):
                    close[0] = enemy.x
                
                if abs(self.y - enemy.y) < abs(self.y - close[1]):
                    close[1] = enemy.y

        separation_vector = norm(separation_vector)
        
        #print(f"seperation_vector: {separation_vector}")

        # print(f"SEP X: {separation_vector[0]} SEP Y: {separation_vector[1]}")

        # Apply separation force (adjust the weight based on desired strength)
        '''
        separation_weight = 50
        final_move_x = int(separation_vector[0] * TILE_SIZE * separation_weight)
        final_move_y = int(separation_vector[1] * TILE_SIZE * separation_weight)
        '''
        
        final_move_x = 0
        final_move_y = 0
        # _________________________________________________________________________________________________________________________

        # CHECK WHICH DIRECTION THE PLAYER IS MAINLY GOING TOWARDS AND UPDATE THE LAST_DIRECTION ATTRIBUTE
        # _________________________________________________________________________________________________________________________
        if abs(horizontal_component) > 0.8:
            if not close_enough:
                final_move_x += int(direction_vector[0] * TILE_SIZE)
            if direction_vector_ori[0] > 0: 
                self.last_direction = 'r'
            elif direction_vector_ori[0] < 0:
                self.last_direction = 'l'

        elif abs(vertical_component) > 0.8:
            if not close_enough:
                final_move_y += int(direction_vector[1] * TILE_SIZE)
            if direction_vector_ori[1] < 0: 
                self.last_direction = 'u'
            elif direction_vector_ori[1] > 0:
                self.last_direction = 'd'

        else: 
            if not close_enough:
                final_move_x += int(direction_vector[0] * TILE_SIZE)
                final_move_y += int(direction_vector[1] * TILE_SIZE)

            if direction_vector_ori[0] > 0: 
                if direction_vector_ori[1] < 0: 
                    self.last_direction = 'ru'
                else: 
                    self.last_direction = 'rd'
            elif direction_vector_ori[0] < 0: 
                if direction_vector_ori[1] < 0: 
                    self.last_direction = 'lu'
                else: 
                    self.last_direction = 'ld'

        self.degrees = getDeg(self.last_direction)
        # _________________________________________________________________________________________________________________________

        # CALCULATE THE NEW POSITION (TILE_X AND TILE_Y ARE THE NEW POSITIONS AND THE FANCY MATH MAKES SURE THEY MOVE DISCREETLY) 
        # _________________________________________________________________________________________________________________________

        tile_x = self.px_x
        tile_y = self.px_y

        if abs(final_move_x) > 0:
            tile_x = int((self.px_x + final_move_x + (TILE_SIZE // 2) - 1) // TILE_SIZE) * TILE_SIZE
            if tile_x == self.px_x:
                tile_x = int((self.px_x + final_move_x - (TILE_SIZE // 2) - 1) // TILE_SIZE) * TILE_SIZE
            
        if abs(final_move_y) > 0:
            tile_y = int((self.px_y + final_move_y + (TILE_SIZE // 2) - 1) // TILE_SIZE) * TILE_SIZE
            if tile_y == self.px_y:
                tile_y = int((self.px_y + final_move_y - (TILE_SIZE // 2) - 1) // TILE_SIZE) * TILE_SIZE
        # _________________________________________________________________________________________________________________________

        # CHECK THAT THE NEW POSITION IS IN BOUNDS AND THAT IT IS  NOT WATER (DEST_ROW AND DEST_COL ARE THE LIST INDEXES) AND SHOOT IF IT IS IN RANGE
        # _________________________________________________________________________________________________________________________
        diff = [(self.x * TILE_SIZE) - tile_x, (self.y * TILE_SIZE) - tile_y]
        
        dx = 0
        dy = 0

        if "l" in self.last_direction:
            dx = self.speed * -1
        
        elif "r" in self.last_direction:
            dx = self.speed
        
        if "d" in self.last_direction:
            dy = self.speed
        
        elif "u" in self.last_direction: 
            dy = self.speed * -1

        new_x = self.x + dx
        new_y = self.y + dy

        sep = calcVector([self.x, self.y], close)

        allow = inMap(self.x, self.y, self.last_direction, self.size)

        if not close_enough and allow and map_tiles[int(new_y // 1)][int(new_x // 1)].walkable:
            target = random.choice([4, 13])
            if random.random() < .3 or (abs(sep[0]) > target or abs(sep[1]) > target):
                self.x = new_x
                self.y = new_y
                self.walked = True

        '''
        if diff[0] != 0 and diff[1] != 0:
            dest_row = tile_x // TILE_SIZE
            dest_col = tile_y // TILE_SIZE

            if 0 <= dest_row and dest_row < MAP_RC[0] and 0 <= dest_col and dest_col < MAP_RC[1]:
                if map_tiles[dest_col][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y = tile_y
                    
                    self.x = dest_row
                    self.y = dest_col

                elif map_tiles[self.px_y // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    self.x = dest_row

                elif map_tiles[dest_col][self.px_x // TILE_SIZE].walkable:
                    self.px_y = tile_y
                    self.y = dest_col

                else:
                    pass

            else:
                print(f"npc.move: 1")

        elif diff[0] != 0:

            dest_row = tile_x // TILE_SIZE

            if 0 <= dest_row and dest_row < MAP_RC[0]:
                if map_tiles[self.px_y // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x                    
                    self.x = dest_row

                elif map_tiles[(self.px_y + TILE_SIZE) // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y += TILE_SIZE
                    
                    self.x = dest_row
                    self.y = self.px_y // TILE_SIZE

                elif map_tiles[(self.px_y - TILE_SIZE) // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y -= TILE_SIZE

                    self.x = dest_row
                    self.y = self.px_y // TILE_SIZE
        
                else:
                    pass

            else:
                print(f"npc.move: 2")

        elif diff[1] != 0:
            dest_col = tile_y // TILE_SIZE

            if 0 <= dest_col and dest_col < MAP_RC[1]:
                if map_tiles[dest_col][self.px_x // TILE_SIZE].walkable:
                    self.px_y = tile_y
                    self.y = dest_col

                elif map_tiles[dest_col][(self.px_x + TILE_SIZE) // TILE_SIZE].walkable:
                    self.px_x += TILE_SIZE
                    self.px_y = tile_y

                    self.x = self.px_x // TILE_SIZE
                    self.y = dest_col

                elif map_tiles[dest_col][(self.px_x + TILE_SIZE) // TILE_SIZE].walkable:
                    self.px_x += TILE_SIZE
                    self.px_y = tile_y

                    self.x = self.px_x // TILE_SIZE
                    self.y = dest_col

                else:
                    pass
            
            else:
                print(f"npc.move: 3")

        elif diff[0] == 0 and diff[1] == 0:
            print(f"nothing")
            self.walked = False
        '''

        if in_range and self.team != "player":
            self.shoot(moving_list)
        # _________________________________________________________________________________________________________________________  

    def build(self, map_tiles):
        # Get the current position of the enemy

        time_delta = checkTime(self.next_wood, self.wood_cooldown)
        if time_delta == -1: 
            return
        else:
            self.next_wood = time_delta

        inBounds = inMap(self.px_x, self.px_y, self.last_direction, self.size)

        # Check the last direction and create a brown tile in that direction
        # DIAGONLS
        if self.last_direction == 'lu' and inBounds and map_tiles[self.px_y - 1][self.px_x - 1].walkable:
            map_tiles[self.px_y - 1][self.px_x - 1] = Tile((self.px_x - 1) * TILE_SIZE, (self.px_y - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ld' and inBounds and map_tiles[self.px_y + 1][self.px_x - 1].walkable:
            map_tiles[self.px_y + 1][self.px_x - 1] = Tile((self.px_x - 1) * TILE_SIZE, (self.px_y + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'rd' and inBounds and map_tiles[self.px_y + 1][self.px_x + 1].walkable:
            map_tiles[self.px_y + 1][self.px_x + 1] = Tile((self.px_x + 1) * TILE_SIZE, (self.px_y + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ru' and inBounds and map_tiles[self.px_y - 1][self.px_x + 1].walkable:
            map_tiles[self.px_y - 1][self.px_x + 1] = Tile((self.px_x + 1) * TILE_SIZE, (self.px_y - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        # CARDINALS
        elif self.last_direction == 'r' and inBounds and map_tiles[self.px_y][self.px_x + 1].walkable:
            map_tiles[self.px_y][self.px_x + 1] = Tile((self.px_x + 1) * TILE_SIZE, self.px_y * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'l' and inBounds and map_tiles[self.px_y][self.px_x - 1].walkable:
            map_tiles[self.px_y][self.px_x - 1] = Tile((self.px_x - 1) * TILE_SIZE, self.px_y * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'd' and inBounds and map_tiles[self.px_y + 1][self.px_x].walkable:
            map_tiles[self.px_y + 1][self.px_x] = Tile(self.px_x * TILE_SIZE, (self.px_y + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'u' and inBounds and map_tiles[self.px_y - 1][self.px_x].walkable:
            map_tiles[self.px_y - 1][self.px_x] = Tile(self.px_x * TILE_SIZE, (self.px_y - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])
            
    def shoot(self, moving_list):

        time_delta = checkTime(self.next_fireball, self.fireball_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_fireball = time_delta

        #print(f"shoot: x: {self.x}, y: {self.y}")
        
        inBounds = inMap(self.x, self.y, self.last_direction, self.size)

        moving_list.append(MovingObject((self.x + self.aim[self.last_direction][0]), (self.y + self.aim[self.last_direction][1]), TILE_SIZE, [255, 0, 0], self.last_direction, "enemy"))
