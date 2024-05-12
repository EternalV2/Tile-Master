import pygame
import random

from global_functions import *
from mapy import Map
from tile import Tile
from player import Player
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size, enemyFPS):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size 
        self.enemyFPS = enemyFPS

        self.last_direction = "u"

        self.next_frame_time = 1
        self.enemyFPS = enemyFPS * 2

        self.next_fireball = 1
        self.fireball_cooldown = enemyFPS * 6

        self.next_animation = 1
        self.animation_time = enemyFPS

        self.image = pygame.image.load("img/hat/hat_u.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

        self.animStack = []
        self.inMotion = 0

        self.degrees = getDeg(self.last_direction)

        self.next_wood = 1
        self.wood_cooldown = 1000

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200
        
        self.emitter = ParticleEmitter(x, y, 10)

    def updateD(self, moving_list):

        # CHECK TIME ______________________________________________________________________________________________________________
        time_delta = checkTime(self.next_animation, self.animation_time)
        if time_delta == -1:
            return
        else:
            self.next_animation = time_delta
        # ________________________________________________________________________________________________________________________

        enemy_row = self.x // TILE_SIZE
        enemy_col = self.y // TILE_SIZE

        # IDLE ____________________________________________________________________________________________________________________
        if not self.animStack:
            if len(self.last_direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load("img/hat/hat_ru.png"), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load("img/hat/hat_u.png"), self.degrees)
            self.inMotion = 0
        # _________________________________________________________________________________________________________________________

        # CAST FIREBALL ___________________________________________________________________________________________________________
        else:
            if len(self.last_direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load(self.animStack.pop()), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load(self.animStack.pop()), self.degrees)

            self.inMotion = 1
        # _________________________________________________________________________________________________________________________


    def move(self, player, moving_list, all_enemies, map_tiles):
        # CHECK THAT THE ENEMY IS FOLLOWING HIS FPS
        # _________________________________________________________________________________________________________________________
        time_delta = checkTime(self.next_frame_time, self.enemyFPS)
        if time_delta == -1:
            return
        else:
            self.next_frame_time = time_delta
        # _________________________________________________________________________________________________________________________

        # IMPLEMENT RANDOM MOTION & MAKE SURE IT IS IN THE MAP
        # _________________________________________________________________________________________________________________________
        rand_move = 0

        if random.random() > .99:
            if basicBounds(self.x - TILE_SIZE, self.y) and map_tiles[self.y // TILE_SIZE][(self.x - TILE_SIZE)// TILE_SIZE].color != [58, 124, 242]:
                self.x -= TILE_SIZE
                return
    
        if random.random() > .99:
            rand_move = self.x + TILE_SIZE
            if basicBounds(self.x + TILE_SIZE, self.y) and map_tiles[self.y // TILE_SIZE][(self.x + TILE_SIZE)// TILE_SIZE].color != [58, 124, 242]:
                self.x += TILE_SIZE
                return

        if random.random() > .99:
            if basicBounds(self.x, self.y + TILE_SIZE) and map_tiles[(self.y + TILE_SIZE)// TILE_SIZE][(self.x) // TILE_SIZE].color != [58, 124, 242]:
                self.y += TILE_SIZE
                return

        if random.random() > .99:
            if basicBounds(self.x, self.y - TILE_SIZE) and map_tiles[(self.y - TILE_SIZE)// TILE_SIZE][self.x // TILE_SIZE].color != [58, 124, 242]:
                self.y -= TILE_SIZE
                return
        # _________________________________________________________________________________________________________________________

        # CALCULATE THE VECTOR, DISTANCE, AND NORMALIZED VECTOR FROM THE ENEMEY TO THE PLAYER,
        # WE USE THE ORIGINAL VECTOR TO CALCULATE THE DIRECTION AND LAST_DIRECITON OF THE PLAYER LATER. 
        # _________________________________________________________________________________________________________________________
        direction_vector_ori = calcVector([player.x, player.y], [self.x, self.y])
        distance = calcDist(direction_vector_ori)
        direction_vector = norm(direction_vector_ori)

        if distance == 0:
            return
        # _________________________________________________________________________________________________________________________

        # EXTRACT THE HORIZONTAL AND VERTICAL COMPONENTS AND SEE IF THE ENEMY IS WITHIN ATTACKING RANGE OR IF THE ENEMY SHOULD STOP MOVING TOWARDS THE PLAYER
        # _________________________________________________________________________________________________________________________
        horizontal_component = direction_vector[0]
        vertical_component = direction_vector[1]

        in_range = 0
        close_enough = 0

        if distance < 200:
            in_range = 1
            if distance < 60:
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
                curr_vector = calcVector([enemy.x, enemy.y], [self.x, self.y])
                distance_to_enemy = calcDist(curr_vector)

                separation_distance = 70

                if distance_to_enemy < separation_distance:
                    separation_vector[0] += self.x - enemy.x
                    separation_vector[1] += self.y - enemy.y
        
        separation_vector = norm(separation_vector)

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
        tile_x = self.x
        tile_y = self.y

        if abs(final_move_x) > 0:
            tile_x = int((self.x + final_move_x + 3) // TILE_SIZE) * TILE_SIZE
            if tile_x == self.x:
                tile_x = int((self.x + final_move_x - 3) // TILE_SIZE) * TILE_SIZE
            
        if abs(final_move_y) > 0:
            tile_y = int((self.y + final_move_y + 3) // TILE_SIZE) * TILE_SIZE
            if tile_y == self.y:
                tile_y = int((self.y + final_move_y - 3) // TILE_SIZE) * TILE_SIZE
        # _________________________________________________________________________________________________________________________

        # CHECK THAT THE NEW POSITION IS IN BOUNDS AND THAT IT IS  NOT WATER (DEST_ROW AND DEST_COL ARE THE LIST INDEXES) AND SHOOT IF IT IS IN RANGE
        # _________________________________________________________________________________________________________________________
        diff = [self.x - tile_x, self.y - tile_y]

        if diff[0] != 0 and diff[1] != 0:
            dest_row = tile_x // TILE_SIZE
            dest_col = tile_y // TILE_SIZE

            if 0 <= tile_x and tile_x < WIDTH and 0 <= tile_y and tile_y < HEIGHT:
                if map_tiles[dest_col][dest_row].color != [58, 124, 242]:
                    self.x = tile_x
                    self.y = tile_y
                    self.rect.center = [self.x, self.y]

                elif map_tiles[self.y // TILE_SIZE][dest_row].color != [58, 124, 242]:
                    self.x = tile_x
                    self.rect.center = [self.x, self.y]

                elif map_tiles[dest_col][self.x // TILE_SIZE].color != [58, 124, 242]:
                    self.y = tile_y
                    self.rect.center = [self.x, self.y]

                else: 
                    self.build(map_tiles)

        elif diff[0] != 0:
            dest_row = tile_x // TILE_SIZE
            
            if 0 <= tile_x and tile_x < WIDTH:
                if map_tiles[self.y // TILE_SIZE][dest_row].color != [58, 124, 242]:
                    self.x = tile_x
                    self.rect.center = [self.x, self.y]

                elif map_tiles[(self.y + TILE_SIZE) // TILE_SIZE][dest_row].color != [58, 124, 242]:
                    self.x = tile_x
                    self.y += TILE_SIZE
                    self.rect.center = [self.x, self.y]

                elif map_tiles[(self.y - TILE_SIZE) // TILE_SIZE][dest_row].color != [58, 124, 242]:
                    self.x = tile_x
                    self.y -= TILE_SIZE
                    self.rect.center = [self.x, self.y]
        
                else:
                    self.build(map_tiles)

        elif diff[1] != 0:
            dest_col = tile_y // TILE_SIZE

            if  0 <= tile_y and tile_y < HEIGHT:
                if map_tiles[dest_col][self.x // TILE_SIZE].color != [58, 124, 242]:
                    self.y = tile_y
                    self.rect.center = [self.x, self.y]

                elif map_tiles[dest_col][(self.x + TILE_SIZE) // TILE_SIZE].color != [58, 124, 242]:
                    self.x += TILE_SIZE
                    self.y = tile_y
                    self.rect.center = [self.x, self.y]

                elif map_tiles[dest_col][(self.x + TILE_SIZE) // TILE_SIZE].color != [58, 124, 242]:
                    self.x += TILE_SIZE
                    self.y = tile_y
                    self.rect.center = [self.x, self.y]

                else:
                    self.build(map_tiles)
        
        if in_range:
            self.shoot(moving_list)
        # _________________________________________________________________________________________________________________________  

    def build(self, map_tiles):
        # Get the current position of the enemy

        time_delta = checkTime(self.next_wood, self.wood_cooldown)
        if time_delta == -1: 
            return
        else:
            self.next_wood = time_delta

        enemy_row = self.x // TILE_SIZE
        enemy_col = self.y // TILE_SIZE

        inBounds = inMap(self.x, self.y, self.last_direction, self.size)

        # Check the last direction and create a brown tile in that direction
        # DIAGONLS
        if self.last_direction == 'lu' and inBounds and map_tiles[enemy_col - 1][enemy_row - 1].color == [58, 124, 242]:
            map_tiles[enemy_col - 1][enemy_row - 1] = Tile((enemy_row - 1) * TILE_SIZE, (enemy_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ld' and inBounds and map_tiles[enemy_col + 1][enemy_row - 1].color == [58, 124, 242]:
            map_tiles[enemy_col + 1][enemy_row - 1] = Tile((enemy_row - 1) * TILE_SIZE, (enemy_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'rd' and inBounds and map_tiles[enemy_col + 1][enemy_row + 1].color == [58, 124, 242]:
            map_tiles[enemy_col + 1][enemy_row + 1] = Tile((enemy_row + 1) * TILE_SIZE, (enemy_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ru' and inBounds and map_tiles[enemy_col - 1][enemy_row + 1].color == [58, 124, 242]:
            map_tiles[enemy_col - 1][enemy_row + 1] = Tile((enemy_row + 1) * TILE_SIZE, (enemy_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        # CARDINALS
        elif self.last_direction == 'r' and inBounds and map_tiles[enemy_col][enemy_row + 1].color == [58, 124, 242]:
            map_tiles[enemy_col][enemy_row + 1] = Tile((enemy_row + 1) * TILE_SIZE, enemy_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'l' and inBounds and map_tiles[enemy_col][enemy_row - 1].color == [58, 124, 242]:
            map_tiles[enemy_col][enemy_row - 1] = Tile((enemy_row - 1) * TILE_SIZE, enemy_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'd' and inBounds and map_tiles[enemy_col + 1][enemy_row].color == [58, 124, 242]:
            map_tiles[enemy_col + 1][enemy_row] = Tile(enemy_row * TILE_SIZE, (enemy_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'u' and inBounds and map_tiles[enemy_col - 1][enemy_row].color == [58, 124, 242]:
            map_tiles[enemy_col - 1][enemy_row] = Tile(enemy_row * TILE_SIZE, (enemy_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])
            
    def shoot(self, moving_list):

        time_delta = checkTime(self.next_fireball, self.fireball_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_fireball = time_delta
        
        enemy_row = self.x // TILE_SIZE
        enemy_col = self.y // TILE_SIZE

        inBounds = inMap(self.x, self.y, self.last_direction, self.size)

        if len(self.last_direction) == 2:
            self.animStack.append("img/hat/hat_ru_cast3.png")
            self.animStack.append("img/hat/hat_ru_cast2.png")
            self.animStack.append("img/hat/hat_ru_cast1.png")
        else:            
            self.animStack.append("img/hat/hat_up_cast3.png")
            self.animStack.append("img/hat/hat_up_cast2.png")
            self.animStack.append("img/hat/hat_up_cast1.png")
        
        # DIAGNOLS
        if self.last_direction == 'lu' and inBounds:
            moving_list.append(MovingObject((enemy_row - 3) * TILE_SIZE, (enemy_col - 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "lu", "enemy"))

        elif self.last_direction == 'ld' and inBounds:
            moving_list.append(MovingObject((enemy_row - 2) * TILE_SIZE, (enemy_col + 2) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "ld", "enemy"))

        elif self.last_direction == 'rd' and inBounds:
            moving_list.append(MovingObject((enemy_row + 2) * TILE_SIZE, (enemy_col + 2) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "rd", "enemy"))

        elif self.last_direction == 'ru' and inBounds:
            moving_list.append(MovingObject((enemy_row + 2) * TILE_SIZE, (enemy_col - 2) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "ru", "enemy"))

        # CARDINALS
        elif self.last_direction == 'r' and inBounds:
            moving_list.append(MovingObject((enemy_row + 3) * TILE_SIZE, enemy_col * TILE_SIZE, TILE_SIZE, [255, 0, 0], "r", "enemy"))

        elif self.last_direction == 'l' and inBounds:
            moving_list.append(MovingObject((enemy_row - 3) * TILE_SIZE, enemy_col * TILE_SIZE, TILE_SIZE, [255, 0, 0], "l", "enemy"))

        elif self.last_direction == 'd' and inBounds:
            moving_list.append(MovingObject((enemy_row) * TILE_SIZE, (enemy_col + 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "d", "enemy"))

        elif self.last_direction == 'u' and inBounds:
            moving_list.append(MovingObject((enemy_row) * TILE_SIZE, (enemy_col - 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "u", "enemy"))
