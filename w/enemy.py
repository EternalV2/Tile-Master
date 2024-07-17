import pygame
import random

from global_functions import *
from mapy import Map
from tile import Tile
from player import Player
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter
from obj import Obj

class Enemy(Obj):
    def __init__(self, x, y, size, enemyFPS):
        
        img = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png"

        anim_stack = []

        super().__init__(x, y, size, "u", enemyFPS, enemyFPS * 2, img, anim_stack)

        # PX FOR INTERNAL USE ONLY        
        self.px_x = x * TILE_SIZE
        self.px_y = y * TILE_SIZE

        self.next_fireball = 1
        self.fireball_cooldown = enemyFPS * 6

        self.inMotion = 0

        self.next_wood = 1
        self.wood_cooldown = 1000

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200
        
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
            if len(self.last_direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru.png"), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png"), self.degrees)
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

        if random.random() > 0:
            print(f"crash incoming")
            if basicBounds([self.px_x - 1, self.px_y]) and map_tiles[self.px_y][(self.px_x - 1)].walkable:
                self.px_x -= 1
                return
    
        if random.random() > .99:
            rand_move = self.px_x + 1
            if basicBounds([self.px_x + 1, self.px_y]) and map_tiles[self.px_y][(self.px_x + 1)].walkable:
                self.px_x += 1
                return

        if random.random() > .99:
            if basicBounds([self.px_x, self.px_y + 1]) and map_tiles[(self.px_y + 1)][self.px_x].walkable:
                self.px_y += 1
                return

        if random.random() > .99:
            if basicBounds([self.px_x, self.px_y - 1]) and map_tiles[(self.px_y - 1)][self.px_x].walkable:
                self.px_y -= 1
                return
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

        if distance < 40:
            in_range = 1
            if distance < 10:
                close_enough = 1
            else:
                close_enough = 0 
        else: 
            in_range = 0
            close_enough = 0 
        # _________________________________________________________________________________________________________________________

        # CALCULATE THE SEPERATION VECTOR OF OTHER ENEMIES TO MAKE SURE THEY DONT GROUP UP ON THE SAME TILE AND TYHE APPLY THE SEPERATION FORCE
        # _________________________________________________________________________________________________________________________
        separation_vector = [0, 0]

        for enemy in all_enemies:
            if enemy != self:
                curr_vector = calcVector([enemy.x, enemy.y], [self.px_x, self.px_y])
                distance_to_enemy = calcDist(curr_vector)

                separation_distance = 70

                if distance_to_enemy < separation_distance:
                    separation_vector[0] += self.px_x - enemy.x
                    separation_vector[1] += self.px_y - enemy.y
        
        separation_vector = norm(separation_vector)

        # print(f"SEP X: {separation_vector[0]} SEP Y: {separation_vector[1]}")

        # Apply separation force (adjust the weight based on desired strength)
        separation_weight = .5
        final_move_x = int(separation_vector[0] * TILE_SIZE * separation_weight)
        final_move_y = int(separation_vector[1] * TILE_SIZE * separation_weight)
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

        # print(f"FINAL MOVE X: {final_move_x}, FINAL MOVE Y: {final_move_y}")
        # print()

        if abs(final_move_x) > 0:
            tile_x = int((self.px_x + final_move_x + 3) // TILE_SIZE) * TILE_SIZE
            if tile_x == self.px_x:
                tile_x = int((self.px_x + final_move_x - 3) // TILE_SIZE) * TILE_SIZE
            
        if abs(final_move_y) > 0:
            tile_y = int((self.px_y + final_move_y + 3) // TILE_SIZE) * TILE_SIZE
            if tile_y == self.px_y:
                tile_y = int((self.px_y + final_move_y - 3) // TILE_SIZE) * TILE_SIZE
        # _________________________________________________________________________________________________________________________

        # CHECK THAT THE NEW POSITION IS IN BOUNDS AND THAT IT IS  NOT WATER (DEST_ROW AND DEST_COL ARE THE LIST INDEXES) AND SHOOT IF IT IS IN RANGE
        # _________________________________________________________________________________________________________________________
        diff = [(self.x * 10) - tile_x, (self.y * 10) - tile_y]


        # print(f"DIFF 0: {diff[0]}, DIFF 1: {diff[1]}")
        # print(f"SELF X: {self.x}, SELF Y: {self.y}")
        # print(f"TILE X: {tile_x}, TILE Y: {tile_y}")
        # print()

        # print(f"PLAYER X: {player.x}, PLAYER Y: {player.y}")
        # print()
        
        if diff[0] != 0 and diff[1] != 0:
            dest_row = tile_x // TILE_SIZE
            dest_col = tile_y // TILE_SIZE

            #if 0 <= tile_x and tile_x < WIDTH and 0 <= tile_y and tile_y < HEIGHT:
            if 0 <= dest_row and dest_row < MAP_RC[0] and 0 <= dest_col and dest_col < MAP_RC[1]:
                if map_tiles[dest_col][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y = tile_y
                    
                    self.x = dest_row
                    self.y = dest_col
                    
                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[self.px_y // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    
                    self.x = dest_row
                    
                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[dest_col][self.px_x // TILE_SIZE].walkable:
                    self.px_y = tile_y
                    
                    self.y = dest_col
                    
                    #self.rect.center = [self.px_x, self.px_y]

                else:
                    print("BUILD") 
                    #self.build(map_tiles)

            else:
                print("1")

        elif diff[0] != 0:

            dest_row = tile_x // TILE_SIZE
            
            # print(f"X MOMENT: {dest_row}")

            #if 0 <= tile_x and tile_x < WIDTH:
            if 0 <= dest_row and dest_row < MAP_RC[0]:
                if map_tiles[self.px_y // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    
                    self.x = dest_row
                    
                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[(self.px_y + TILE_SIZE) // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y += TILE_SIZE
                    
                    self.x = dest_row
                    self.y = self.px_y // TILE_SIZE

                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[(self.px_y - TILE_SIZE) // TILE_SIZE][dest_row].walkable:
                    self.px_x = tile_x
                    self.px_y -= TILE_SIZE

                    self.x = dest_row
                    self.y = self.px_y // TILE_SIZE

                    #self.rect.center = [self.px_x, self.px_y]
        
                else:
                    print("BUILD")
                    #self.build(map_tiles)
            else:
                print("2")

        elif diff[1] != 0:
            dest_col = tile_y // TILE_SIZE

            #if  0 <= tile_y and tile_y < HEIGHT:
            if 0 <= dest_col and dest_col < MAP_RC[1]:
                if map_tiles[dest_col][self.px_x // TILE_SIZE].walkable:
                    self.px_y = tile_y

                    self.y = dest_col
                    
                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[dest_col][(self.px_x + TILE_SIZE) // TILE_SIZE].walkable:
                    self.px_x += TILE_SIZE
                    self.px_y = tile_y

                    self.x = self.px_x // TILE_SIZE
                    self.y = dest_col

                    #self.rect.center = [self.px_x, self.px_y]

                elif map_tiles[dest_col][(self.px_x + TILE_SIZE) // TILE_SIZE].walkable:
                    self.px_x += TILE_SIZE
                    self.px_y = tile_y

                    self.x = self.px_x // TILE_SIZE
                    self.y = dest_col

                    #self.rect.center = [self.px_x, self.px_y]

                else:
                    print("BUILD")
                    #self.build(map_tiles)
            
            else:
                print("3")
        
        if in_range:
            print("SHOT")
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
        
        inBounds = inMap(self.x, self.y, self.last_direction, self.size)

        if len(self.last_direction) == 2:
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast3.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast2.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast1.png")
        else:            
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast3.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast2.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast1.png")
        
        # DIAGNOLS
        if self.last_direction == 'lu' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE - 3), (self.px_y // TILE_SIZE - 3), TILE_SIZE, [255, 0, 0], "lu", "enemy"))

        elif self.last_direction == 'ld' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE - 2), (self.px_y // TILE_SIZE + 2), TILE_SIZE, [255, 0, 0], "ld", "enemy"))

        elif self.last_direction == 'rd' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE + 2), (self.px_y // TILE_SIZE + 2), TILE_SIZE, [255, 0, 0], "rd", "enemy"))

        elif self.last_direction == 'ru' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE + 2), (self.px_y // TILE_SIZE - 2), TILE_SIZE, [255, 0, 0], "ru", "enemy"))

        # CARDINALS
        elif self.last_direction == 'r' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE + 3), self.px_y // TILE_SIZE, TILE_SIZE, [255, 0, 0], "r", "enemy"))

        elif self.last_direction == 'l' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE - 3), self.px_y // TILE_SIZE, TILE_SIZE, [255, 0, 0], "l", "enemy"))

        elif self.last_direction == 'd' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE), (self.px_y // TILE_SIZE + 3), TILE_SIZE, [255, 0, 0], "d", "enemy"))

        elif self.last_direction == 'u' and inBounds:
            moving_list.append(MovingObject((self.px_x // TILE_SIZE), (self.px_y // TILE_SIZE - 3), TILE_SIZE, [255, 0, 0], "u", "enemy"))
