import pygame
import random

from mapy import Map
from tile import Tile
import math

# Set the tile size
TILE_SIZE = 10
WIDTH = 1350
HEIGHT = 750
SPAWN = (100, 90)
# CENTER OF MAP
#SPAWN = (94, 52)
MAP_SIZE = (1890, 1050)
#MAP_SIZE = (2200, 1500)
MAP_RC = (MAP_SIZE[0] // TILE_SIZE, MAP_SIZE[1] // TILE_SIZE)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

ORI_MOUSE_POS = [WIDTH // (2 * TILE_SIZE), HEIGHT // (2 * TILE_SIZE)]

IMG_DIRECTORY =  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/"

MAP_TXT = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/map.txt"

def basicBounds(rcTuple):
    if 0 <= rcTuple[0] and rcTuple[0] < MAP_RC[0] and 0 <= rcTuple[1] and rcTuple[1] < MAP_RC[1]:
        return True
    else:
        #print(f"lol")
        return False

'''
# BASIC BOUNDS TAKES THE PIXEL POSITION AND CHECKS THAT ITS IN THE MAP
def basicBounds(x, y):
    if 0 <= x and x < WIDTH and 0 <= y and y < HEIGHT:
        return True
    else:
        return False
'''

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
    #print(f"LAST DIRECTION: {last_direction}, X: {x}, Y: {y}")
    allow = 0

    # Check if the new position is on land (not water) and that the player is within the map bounds.
    if last_direction == "lu":
        if y > 0 and x > 0:
            allow = 1

    elif last_direction == "ld":
        if y < MAP_RC[1] - 2 and x > 0:
            allow = 1

    elif last_direction == "rd":
        if y < MAP_RC[1] - 2 and x < MAP_RC[0] - 2:
            allow = 1

    elif last_direction == "ru":
        if y > 0 and x < MAP_RC[0] - 2:
            allow = 1

    elif last_direction == "l":
        if x > 0:
            allow = 1

    elif last_direction == "r":
        if x < MAP_RC[0] - 2:
            allow = 1

    elif last_direction == "u":
        if y > 0:
            allow = 1

    elif last_direction == "d":
        if y < MAP_RC[1] - 2:
            allow = 1

    return allow


def wasdKeys(key, keys, player, gameMap):
    # Implement actions based on held keys
    if key == pygame.K_a:

        if keys[pygame.K_a] and keys[pygame.K_w]:
            player.move(-1, -1, gameMap.tiles)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            player.move(-1, 1, gameMap.tiles)
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            return
        else:
            player.move(-1, 0, gameMap.tiles)

    elif key == pygame.K_d:

        if keys[pygame.K_d] and keys[pygame.K_w]:
            player.move(1, -1, gameMap.tiles)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            player.move(1, 1, gameMap.tiles)
        elif keys[pygame.K_d] and keys[pygame.K_a]:
            return
        else:
            player.move(1, 0, gameMap.tiles)

    elif key == pygame.K_w:

        if keys[pygame.K_w] and keys[pygame.K_a]:
            player.move(-1, -1, gameMap.tiles)
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            player.move(1, -1, gameMap.tiles)
        elif keys[pygame.K_w] and keys[pygame.K_s]:
            return
        else:
            player.move(0, -1, gameMap.tiles)

    elif key == pygame.K_s:

        if keys[pygame.K_s] and keys[pygame.K_a]:
            player.move(-1, 1, gameMap.tiles)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            player.move(1, 1, gameMap.tiles)
        elif keys[pygame.K_s] and keys[pygame.K_w]:
            return
        else:
            player.move(0, 1, gameMap.tiles)

# DOES NOT HANDLE IMG_NAMES
def drawRectArr(x, y, brush_size, img_arr, name_arr, game_map):
    print(f"START DRAW ARR {game_map.tiles[x][y].image}, BRUSH: {brush_size}")
    # TODO MAKE IT OBVIOUS that img_arr == None MEANS THAT THE CURSOR IS OFF MAP
    if img_arr == None: 
        return

    start_row, end_row = max(0, x - brush_size + 1), min(MAP_RC[1], x + brush_size)
    start_col, end_col = max(0, y - brush_size + 1), min(MAP_RC[0], y + brush_size)

    # TODO STATE THAT I AND J ARE EXPLICITLY POINTERS OF THE IMG_ARRAY, NOT THE ROW OR COL PTERS
    # IF THEY WHERE EQUAL TO ROW AND COL, THERE WOULD BE AN OUT OF BOUNDS EXCEPTION
    i = j = 0

    for l in range(len(img_arr)):
        for r in range(len(img_arr[0])):
            print("ASDSAADASD", img_arr[l][r])

    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            game_map.tiles[row][col].image = img_arr[i][j]
            game_map.tiles[row][col].name = name_arr[i][j]
            j += 1
        j = 0
        i += 1
    print(f"END DRAW ARR{game_map.tiles[x][y].image}, BRUSH: {brush_size}")

def drawRectOne(x, y, brush_size, img, img_name, game_map):

    start_row, end_row = max(0, x - brush_size + 1), min(MAP_RC[1], x + brush_size)
    start_col, end_col = max(0, y - brush_size + 1), min(MAP_RC[0], y + brush_size)

    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            game_map.tiles[row][col].image = img
            game_map.tiles[row][col].name = img_name


def drawRectOneS(x, y, brush_size, img, img_name, game_map):

    start_row, end_row = max(0, x - brush_size + 1), min(MAP_RC[1], x + brush_size)
    start_col, end_col = max(0, y - brush_size + 1), min(MAP_RC[0], y + brush_size)

    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            game_map.tiles[row][col].image = img
            game_map.tiles[row][col].name = img_name


def copyRect(x, y, brush_size, game_map):
    print(f"\nSTART COPY {game_map.tiles[x][y].image}, BRUSH: {brush_size}")
    start_row, end_row = max(0, x - brush_size + 1), min(MAP_RC[1], x + brush_size)
    start_col, end_col = max(0, y - brush_size + 1), min(MAP_RC[0], y + brush_size)

    #print(f"Start Row: {start_row}, End Row: {end_row}")
    #print(f"Start Col: {start_col}, End Col: {end_col}")

    name_arr = [[None for _ in range(end_col - start_col)] for _ in range(end_row - start_row)]
    img_arr = [[None for _ in range(end_col - start_col)] for _ in range(end_row - start_row)]

    # TODO STATE THAT I AND J ARE EXPLICITLY POINTERS OF THE IMG_ARRAY, NOT THE ROW OR COL PTERS
    # IF THEY WHERE EQUAL TO ROW AND COL, THERE WOULD BE AN OUT OF BOUNDS EXCEPTION
    i = j = 0

    print(f"SAVE ME: {len(img_arr)}, {len(img_arr[0])}")
    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            print(game_map.tiles[row][col].image)

    x = 0
    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            name_arr[i][j] = game_map.tiles[row][col].name
            img_arr[i][j] = game_map.tiles[row][col].image
            #print(row, col)
            #print(type(game_map.tiles[row][col].image))
            j += 1
        j = 0
        i += 1
        x+=1 
    print(f"XXXXXX {x}")
    print(f"END COPY {game_map.tiles[x][y].image}, BRUSH: {brush_size}\n")


    c = 0
    u = 0
    print(f"FUCK ME: {len(img_arr)}, {len(img_arr[0])}")
    for row in range(start_row, end_row, 1):
        for col in range(start_col, end_col, 1):
            print(img_arr[c][u])
            u += 1
        u =0
        c+=1 


    return name_arr, img_arr