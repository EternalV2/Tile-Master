import pygame
import random

from mapy import Map
from tile import Tile
import math

# Set the tile size
TILE_SIZE = 10
WIDTH = 1350
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# BASIC BOUNDS TAKES THE PIXEL POSITION AND CHECKS THAT ITS IN THE MAP
def basicBounds(x, y):
    if 0 <= x and x < WIDTH and 0 <= y and y < HEIGHT:
        return True
    else:
        return False

def calcVector(pos_1, pos_2):
    res = []
    res.append(pos_1[0] - pos_2[0])
    res.append(pos_1[1] - pos_2[1])
    return res

def norm(vector):
    # Normalize the vector to get a unit vector
    magnitude = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
    if magnitude != 0:
        res_vector = [vector[0] / magnitude, vector[1] / magnitude]
        return res_vector
    else:
        return vector

def calcDist(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def checkTime(next_event_time, event_delay):
    time_now = pygame.time.get_ticks()

    if time_now < next_event_time:
        return -1

    return time_now + event_delay


def getDeg(last_direction):
    if last_direction == "lu":
        return 45

    elif last_direction == "ld":
        return 135

    elif last_direction == "ru":
        return 315

    elif last_direction == "rd":
        return 225

    elif last_direction == "r":
        return 270

    elif last_direction == "l":
        return 90

    elif last_direction == "d":
        return 180

    elif last_direction == "u":
        return 0

    return -1

# IN MAP TAKES THE DIRECTION AND THE PIXEL COORDINATES AND CHECKS THAT ITS IN THE MAP
def inMap(x, y, last_direction, size):
    allow = 0

    # Check if the new position is on land (not water) and that the player is within the map bounds.
    if last_direction == "lu":
        if y > 0 and x > 0:
            allow = 1

    elif last_direction == "ld":
        if y < HEIGHT - size - TILE_SIZE and x > 0:
            allow = 1

    elif last_direction == "rd":
        if y < HEIGHT - size - TILE_SIZE and x < WIDTH - size - TILE_SIZE:
            allow = 1

    elif last_direction == "ru":
        if y > 0 and x < WIDTH - size - TILE_SIZE:
            allow = 1

    elif last_direction == "l":
        if x > 0:
            allow = 1

    elif last_direction == "r":
        if x < WIDTH - size - TILE_SIZE:
            allow = 1

    elif last_direction == "u":
        if y > 0:
            allow = 1

    elif last_direction == "d":
        if y < HEIGHT - size - TILE_SIZE:
            allow = 1

    if not allow:
        # print("NOPE")
        pass
    else:
        # print("ALL GOOD")
        pass

    return allow


def wasdKeys(key, keys, player, gameMap):
    # Implement actions based on held keys
    if key == pygame.K_a:

        if keys[pygame.K_a] and keys[pygame.K_w]:
            player.move(-TILE_SIZE, -TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            player.move(-TILE_SIZE, TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            return
        else:
            player.move(-TILE_SIZE, 0, gameMap.tiles)

    elif key == pygame.K_d:

        if keys[pygame.K_d] and keys[pygame.K_w]:
            player.move(TILE_SIZE, -TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            player.move(TILE_SIZE, TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_d] and keys[pygame.K_a]:
            return
        else:
            player.move(TILE_SIZE, 0, gameMap.tiles)

    elif key == pygame.K_w:

        if keys[pygame.K_w] and keys[pygame.K_a]:
            player.move(-TILE_SIZE, -TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            player.move(TILE_SIZE, -TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_w] and keys[pygame.K_s]:
            return
        else:
            player.move(0, -TILE_SIZE, gameMap.tiles)

    elif key == pygame.K_s:

        if keys[pygame.K_s] and keys[pygame.K_a]:
            player.move(-TILE_SIZE, TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            player.move(TILE_SIZE, TILE_SIZE, gameMap.tiles)
        elif keys[pygame.K_s] and keys[pygame.K_w]:
            return
        else:
            player.move(0, TILE_SIZE, gameMap.tiles)
