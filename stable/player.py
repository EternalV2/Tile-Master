import pygame

from global_functions import *
from mapy import Map
from moving_object import MovingObject
from particle_emitter import Particle, ParticleEmitter

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, playerFPS):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.last_direction = "u"

        self.health = 3
        self.next_hit = 1
        self.hit_cooldown = 200

        self.next_wood = 1
        self.wood_cooldown = 500


        # ANIMATION TIMING ___________________________________________________________________________________________________________
        self.next_frame_time = 1
        self.playerFPS = playerFPS * 1.35

        self.next_fireball = 1
        self.fireball_cooldown = playerFPS * 6

        self.next_animation = 1
        self.animation_time = playerFPS
        # ANIMATION TIMING ___________________________________________________________________________________________________________

        self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

        self.animStack = []
        self.inMotion = 0

        self.degrees = getDeg(self.last_direction)

        self.emitter = ParticleEmitter(x, y, 10)

    def updateD(self, moving_list):

        # CHECK TIME ______________________________________________________________________________________________________________
        time_delta = checkTime(self.next_animation, self.animation_time)
        if time_delta == -1:
            return
        else:
            self.next_animation = time_delta
        # ________________________________________________________________________________________________________________________

        player_row = self.x // TILE_SIZE
        player_col = self.y // TILE_SIZE

        # IDLE ____________________________________________________________________________________________________________________
        if not self.animStack:
            if len(self.last_direction) == 2:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru.png"), self.degrees+45)
            else:
                self.image = pygame.transform.rotate(pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_u.png"), self.degrees)
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

    def move(self, dx, dy, map_tiles):
        new_x = self.x + dx
        new_y = self.y + dy

        # Update last_direction based on movement
        if dx < 0 and dy < 0:
            self.last_direction = 'lu'
        elif dx < 0 and dy > 0:
            self.last_direction = 'ld'
        elif dx > 0 and dy < 0:
            self.last_direction = 'ru'
        elif dx > 0 and dy > 0:
            self.last_direction = 'rd'
        elif dx > 0:
            self.last_direction = 'r'
        elif dx < 0:
            self.last_direction = 'l'
        elif dy > 0:
            self.last_direction = 'd'
        elif dy < 0:
            self.last_direction = 'u'

        self.degrees = getDeg(self.last_direction)

        time_delta = checkTime(self.next_frame_time, self.playerFPS)
        if time_delta == -1:
            return
        else:
            self.next_frame_time = time_delta

        allow = inMap(self.x, self.y, self.last_direction, self.size)
        
        if allow and map_tiles[new_y // TILE_SIZE][new_x // TILE_SIZE].color != [58, 124, 242]:
            self.x = new_x
            self.y = new_y
            self.rect.center = [self.x, self.y]

    def build(self, map_tiles):

        time_delta = checkTime(self.next_wood, self.wood_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_wood = time_delta

        # Get the current position of the player
        player_row = self.x // TILE_SIZE
        player_col = self.y // TILE_SIZE

        inBounds = inMap(self.x, self.y, self.last_direction, self.size)

        # Check the last direction and create a brown tile in that direction
        # DIAGONLS
        if self.last_direction == 'lu' and inBounds and map_tiles[player_col - 1][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ld' and inBounds and map_tiles[player_col + 1][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'rd' and inBounds and map_tiles[player_col + 1][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'ru' and inBounds and map_tiles[player_col - 1][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        # CARDINALS
        elif self.last_direction == 'r' and inBounds and map_tiles[player_col][player_row + 1].color == [58, 124, 242]:
            map_tiles[player_col][player_row + 1] = Tile((player_row + 1) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'l' and inBounds and map_tiles[player_col][player_row - 1].color == [58, 124, 242]:
            map_tiles[player_col][player_row - 1] = Tile((player_row - 1) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'd' and inBounds and map_tiles[player_col + 1][player_row].color == [58, 124, 242]:
            map_tiles[player_col + 1][player_row] = Tile(player_row * TILE_SIZE, (player_col + 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

        elif self.last_direction == 'u' and inBounds and map_tiles[player_col - 1][player_row].color == [58, 124, 242]:
            map_tiles[player_col - 1][player_row] = Tile(player_row * TILE_SIZE, (player_col - 1) * TILE_SIZE, TILE_SIZE, [172, 86, 29])

    def shoot(self, map_tiles, moving_list):

        if self.inMotion:
            return

        time_delta = checkTime(self.next_fireball, self.fireball_cooldown)
        if time_delta == -1:
            return
        else:
            self.next_fireball = time_delta
        
        player_row = self.x // TILE_SIZE
        player_col = self.y // TILE_SIZE

        inBounds = inMap(self.x, self.y, self.last_direction, self.size)
        
        if len(self.last_direction) == 2:
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast3.png")
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast2.png")
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_ru_cast1.png")
        else:            
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast3.png")
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast2.png")
            self.animStack.append("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/hat/hat_up_cast1.png")

        # DIAGNOLS
        if self.last_direction == 'lu' and inBounds:
            moving_list.append(MovingObject((player_row - 3) * TILE_SIZE, (player_col - 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "lu", "player"))

        elif self.last_direction == 'ld' and inBounds:
            moving_list.append(MovingObject((player_row - 3) * TILE_SIZE, (player_col + 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "ld", "player"))

        elif self.last_direction == 'rd' and inBounds:
            moving_list.append(MovingObject((player_row + 3) * TILE_SIZE, (player_col + 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "rd", "player"))

        elif self.last_direction == 'ru' and inBounds:
            moving_list.append(MovingObject((player_row + 3) * TILE_SIZE, (player_col - 3) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "ru", "player"))

        # CARDINALS
        elif self.last_direction == 'r' and inBounds:
            moving_list.append(MovingObject((player_row + 4) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [255, 0, 0], "r", "player"))

        elif self.last_direction == 'l' and inBounds:
            moving_list.append(MovingObject((player_row - 4) * TILE_SIZE, player_col * TILE_SIZE, TILE_SIZE, [255, 0, 0], "l", "player"))

        elif self.last_direction == 'd' and inBounds:
            moving_list.append(MovingObject((player_row) * TILE_SIZE, (player_col + 4) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "d", "player"))

        elif self.last_direction == 'u' and inBounds:
            moving_list.append(MovingObject((player_row) * TILE_SIZE, (player_col - 4) * TILE_SIZE, TILE_SIZE, [255, 0, 0], "u", "player"))
