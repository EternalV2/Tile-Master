import pygame

from global_functions import *
from mapy import Map
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter
from camera import Camera 
from obj import Obj

class Player(Obj):
    def __init__(self, x, y, size, playerFPS):

        img = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png"
        anim_stack = []        

        super().__init__(x, y, size, "u", playerFPS, playerFPS * 1.35, img, anim_stack)

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200

        self.next_wood = 1
        self.wood_cooldown = 500

        self.next_fireball = 1
        self.fireball_cooldown = playerFPS * 6

        self.inMotion = 0

    # I THINK updateD HANDLES TE ANIMATION STACK
    def updateD(self, screen, moving_list):

        # CHECK TIME ______________________________________________________________________________________________________________
        time_delta = checkTime(self.next_animation, self.animation_time)
        if time_delta == -1:
            return
        else:
            self.next_animation = time_delta
        # ________________________________________________________________________________________________________________________

        player_row = self.x
        player_col = self.y
        
        # IDLE ____________________________________________________________________________________________________________________
        if not self.anim_stack:
            if len(self.direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru.png"), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png"), self.degrees)
            self.inMotion = 0
        # _________________________________________________________________________________________________________________________

        # CAST FIREBALL ___________________________________________________________________________________________________________
        else:
            if len(self.direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load(self.anim_stack.pop()), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load(self.anim_stack.pop()), self.degrees)

            self.inMotion = 1
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
        
        allow = inMap(self.x, self.y, self.direction, self.size)
        #print("MOVE???? ", allow)
        
        if allow and map_tiles[new_y][new_x].walkable:
            self.x = new_x
            self.y = new_y

    # DISABLED BUILDING
    def build(self, map_tiles):

        time_delta = checkTime(self.next_wood, self.wood_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_wood = time_delta

        # Get the current position of the player
        player_row = self.x
        player_col = self.y

        inBounds = inMap(self.x, self.y, self.direction, self.size)

        # Check the last direction and create a brown tile in that direction
        # DIAGONLS
        if self.direction == 'lu' and inBounds and map_tiles[player_col - 1][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'ld' and inBounds and map_tiles[player_col + 1][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'rd' and inBounds and map_tiles[player_col + 1][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'ru' and inBounds and map_tiles[player_col - 1][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        # CARDINALS
        elif self.direction == 'r' and inBounds and map_tiles[player_col][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'l' and inBounds and map_tiles[player_col][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'd' and inBounds and map_tiles[player_col + 1][player_row].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row] = Tile(player_row * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.direction == 'u' and inBounds and map_tiles[player_col - 1][player_row].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row] = Tile(player_row * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

    def shoot(self, map_tiles, moving_list):

        if self.inMotion:
            return

        time_delta = checkTime(self.next_fireball, self.fireball_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_fireball = time_delta
        
        player_row = self.x
        player_col = self.y

        inBounds = inMap(self.x, self.y, self.direction, self.size)
        
        # FIREBALL CASTING ANIMATION
        # DIAGNOL CASTING
        if len(self.direction) == 2:
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast3.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast2.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast1.png")
        
        # CARDINAL CASTING
        else:            
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast3.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast2.png")
            self.anim_stack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast1.png")

        # DIAGNOLS
        if self.direction == 'lu' and inBounds:
            moving_list.append(MovingObject((player_row - 3), (player_col - 3), TILE_SIZE, [255, 0, 0], "lu", "player"))

        elif self.direction == 'ld' and inBounds:
            moving_list.append(MovingObject((player_row - 3), (player_col + 3), TILE_SIZE, [255, 0, 0], "ld", "player"))

        elif self.direction == 'rd' and inBounds:
            moving_list.append(MovingObject((player_row + 3), (player_col + 3), TILE_SIZE, [255, 0, 0], "rd", "player"))

        elif self.direction == 'ru' and inBounds:
            moving_list.append(MovingObject((player_row + 3), (player_col - 3), TILE_SIZE, [255, 0, 0], "ru", "player"))

        # CARDINALS
        elif self.direction == 'r' and inBounds:
            moving_list.append(MovingObject((player_row + 4), player_col, TILE_SIZE, [255, 0, 0], "r", "player"))

        elif self.direction == 'l' and inBounds:
            moving_list.append(MovingObject((player_row - 4), player_col, TILE_SIZE, [255, 0, 0], "l", "player"))

        elif self.direction == 'd' and inBounds:
            moving_list.append(MovingObject((player_row), (player_col + 4), TILE_SIZE, [255, 0, 0], "d", "player"))

        elif self.direction == 'u' and inBounds:
            moving_list.append(MovingObject((player_row), (player_col - 4), TILE_SIZE, [255, 0, 0], "u", "player"))
