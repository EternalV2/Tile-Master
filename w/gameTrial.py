# STILL LEAKING MEMORY. SLIGHT MEMORY LEAK WITH FIREBALLS??? LEAKING LESS THEN .01 MB WITHOUT THEM. MORE WITH THEM?
# DONT FORGET TO FIX THE LEAK

import pygame
import sys
import random

from global_functions import *
from mapy import Map
from tile import Tile
from player import Player
from moving_object import MovingObject
from enemy import Enemy
from userI import UserI
from camera import Camera
from cursor import Cursor

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Landscape")

ui = UserI(3)

start_time = pygame.time.get_ticks()

# Create objects
gameMap = Map(TILE_SIZE, MAP_SIZE)

'''

for j in range(len(gameMap.tiles[0])):
    if j == 0 or j == 188: 
        #print(j==188 and j!= 0 and j!= 1)
        for i in range(len(gameMap.tiles)):
            gameMap.tiles[i][j].color = [121, 201, 35]
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png")
    elif j % 2 == 0:
        for i in range(len(gameMap.tiles)):
            gameMap.tiles[i][j].color = [121, 201, 35]
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")
    else:
        for i in range(len(gameMap.tiles)):
            gameMap.tiles[i][j].color = [193, 199, 40]
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")

for i in range(len(gameMap.tiles)):
    if i == 0 or i == 104:
        #print(f"LEN: {len(gameMap.tiles)}")
        for j in range(len(gameMap.tiles[0])):
            gameMap.tiles[i][j].color = [121, 201, 35]
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png")
    elif i % 2 == 0:
        for j in range(len(gameMap.tiles[0])):
            gameMap.tiles[i][j].color = [193, 199, 40]
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")

# MAKE A VERTICAL LINE OF WATER
for i in range(len(gameMap.tiles)):
    if i % 3 == 0:
        gameMap.tiles[i][55].walkable = False
        gameMap.tiles[i][55].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png")

'''

gameMap.load(MAP_TXT.format(0))

end_time = pygame.time.get_ticks()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
#print(f"Elapsed Time: {elapsed_time} milliseconds")

player = Player(SPAWN[0], SPAWN[1], 5, 20)
cursor = Cursor(ORI_MOUSE_POS[0], ORI_MOUSE_POS[1])
pygame.mouse.set_pos((ORI_MOUSE_POS[0], ORI_MOUSE_POS[1]))

#print(f"ORI POS X: {ORI_MOUSE_POS[0]}, {ORI_MOUSE_POS[1]}")

camera = Camera(player)


# Main game loop
clock = pygame.time.Clock()

movingList = []

# Dictionary to store key states and timers
key_states = {}
key_start_times = {}

enemy_list = []

# for i in range(1):
#     enemy_list.append(Enemy((150 * i) + 1000, 150 * i + 300, TILE_SIZE, 35))
for i in range(3):
    enemy_list.append(Enemy(28 * i + 28, 52 + (5 * i), TILE_SIZE, 35))

#print()

while True:
    #startTrackMalloc()

    camera.update(gameMap)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            cursor.x, cursor.y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
            #print(f"CURSOR X: {cursor.x}, Y: {cursor.y}")

        # BUILD KEY STATE LIST
        elif event.type == pygame.KEYDOWN:
            # Key is pressed down
            key_states[event.key] = True
            if event.key not in key_start_times:
                key_start_times[event.key] = pygame.time.get_ticks()
            # print(f"Key {pygame.key.name(event.key)} pressed")

        elif event.type == pygame.KEYUP:
            # Key is released
            key_states[event.key] = False
            if event.key in key_start_times:
                del key_start_times[event.key]  # Remove the key from start times

    # Check for held keys and update timers
    for key, state in key_states.items():
        if state:
            wasdKeys(key, keys, player, gameMap)

            if key == pygame.K_SPACE:
                pass
                #player.build(gameMap.tiles)

            elif key == pygame.K_p:
                player.shoot(gameMap.tiles, movingList)

    # Draw map and player
    # gameMap.draw(screen)
    camera.addE(player, screen)
    camera.addMap(0, gameMap)
    camera.renderMap(screen)

    for enemy in enemy_list:
        enemy.move(player, movingList, enemy_list, gameMap.tiles)
        #print(f"ENEMY POS X: {enemy.x}, POS Y: {enemy.y}")
        camera.addE(enemy, screen)

    for obj in movingList:
        camera.addObj(obj, screen)

        brake = 0

        # Attach emitter to player and Enemies

        if obj.rect.colliderect(player.rect):
            if obj.team != "player":
                time_delta = checkTime(player.next_hit, player.hit_cooldown)
                if time_delta != -1:
                    player.health -= 1
                    player.next_hit = time_delta
                    ui.updateHealth(player.health)
                    movingList.remove(obj)
                    player.emitter.x = player.x
                    player.emitter.y = player.y
                    player.emitter.emit_particles_circular(player.x, player.y, 30)
                    continue

        for enemy in enemy_list:
            if obj.rect.colliderect(enemy.rect):
                if obj.team != "enemy":
                    time_delta = checkTime(enemy.next_hit, enemy.hit_cooldown)
                    if time_delta != -1:
                        enemy.health -= 1
                        enemy.next_hit = time_delta
                        if enemy.health == 0:
                            enemy_list.remove(enemy)
                        movingList.remove(obj)
                        enemy.emitter.x = enemy.x
                        enemy.emitter.y = enemy.y
                        enemy.emitter.emit_particles_circular(enemy.x, enemy.y, 30)
                        # Dont double free the same object
                        brake = 1
                        break

        if brake:
            continue

        if obj.move() == -1:
            curr_time = pygame.time.get_ticks()
            if curr_time > obj.delete_time:
                movingList.remove(obj)

    camera.renderObj(screen)
    ui.heart_arr.draw(screen)

    player.updateD(screen, movingList)
    #player.emitter.update([0, 0], [0, 0])
    #player.emitter.draw(screen)

    for enemy in enemy_list:
        enemy.updateD(movingList)
        #enemy.emitter.update()
        #enemy.emitter.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    #endTrackMalloc()