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
from npc import Npc
from userI import UserI, Ui_sprite
from camera import Camera
from cursor import Cursor
from particle_emitter import ParticleEmitter
from ambience import Ambience

import glob

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Procedurally Generated Landscape")


# Load the music file
#pygame.mixer.music.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/fog_el_nakhel.mp3")
#pygame.mixer.music.set_volume(.05)
#pygame.mixer.music.play(loops=-1)
weapon_arr = []
#weapon_arr.append(Ui_sprite("ring", "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/ring/ring_frame.png"))
weapon_arr.append(Ui_sprite("fireball", "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/fireball/fireball_frame.png"))
weapon_arr.append(Ui_sprite("sword", "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/sword/sword_frame.png"))
minimap = Ui_sprite("minimap", "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/minimap/cavern_minimap.png")
ui = UserI(3, weapon_arr, minimap)

start_time = pygame.time.get_ticks()

# Create objects
#gameMap = Map(TILE_SIZE, MAP_SIZE)

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

#print(f"AD: {MAP_TXT.format(0).format(TILE_SIZE)}")

num_map_txts = len(glob.glob(MAP_TXT.format('*')))

for i in range(num_map_txts):
    #print(f"load: {i}")
    frame_list.append(Map(TILE_SIZE, MAP_SIZE))
    frame_list[i].load(MAP_TXT.format(i))

next_frame_time = pygame.time.get_ticks() + 1000

curr_map = frame_list[0]

end_time = pygame.time.get_ticks()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
#print(f"Elapsed Time: {elapsed_time} milliseconds")

aim = {'lu': (-3, -3), 'ld': (-3, 3), 'rd': (3, 3), 'ru': (3, -3), 'r': (4, 0), 'l': (-4, 0), 'd': (0, 4), 'u': (0, -4)}
player = Player(SPAWN[0], SPAWN[1], 5, "gandalf", aim, .35, False, 100, 20)
cursor = Cursor(ORI_MOUSE_POS[0], ORI_MOUSE_POS[1])
pygame.mouse.set_pos((ORI_MOUSE_POS[0], ORI_MOUSE_POS[1]))

#print(f"ORI POS X: {ORI_MOUSE_POS[0]}, {ORI_MOUSE_POS[1]}")

# Main game loop
clock = pygame.time.Clock()

movingList = []

# Dictionary to store key states and timers
key_states = {}
key_start_times = {}

enemy_list = []

#enemy_list.append(Npc(0, 58, TILE_SIZE, "player", "gollum", .75, 35))
#enemy_list.append(Npc(4, 53, TILE_SIZE, "player", "sam", .55, 35))

# for i in range(1):
#     enemy_list.append(Npc((150 * i) + 1000, 150 * i + 300, TILE_SIZE, "enemy", 35))
balrog_aim = {'lu': (-6, 3), 'ld': (-6, 3), 'rd': (5, 3), 'ru': (4, 2), 'r': (4, 2), 'l': (-7, 3), 'd': (0, 5), 'u': (0, -5)}
#enemy_list.append(Npc(12, 30, TILE_SIZE, "enemy", "balrog", balrog_aim, .2, True, 35))
enemy_list.append(Npc(45, 6, TILE_SIZE, "enemy", "balrog", balrog_aim, .2, True, 35))
#enemy_list.append(Npc(110, 40, TILE_SIZE, "enemy", "balrog", balrog_aim, .2, True, 35))

camera = Camera(player, TILE_SIZE)
#print()

# EVENTS IS THE RANGE OF FRAMES YOUR  CURRENTLY ON
# TRANSIT FRAMES ARE FRAMES WHICH ONLY PLAY ONCE
# EVENTS_TIMES ARE THE TIMES BETWEEN EACH FRAME
events = [[0, 2]]
transit_frames = []
events_times = [1000, 1000, 1000]

'''
events = [[0, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7,7], [8, 8]]
transit_frames = [3, 4, 5, 6, 7]
events_times = [1000, 1000, 1000, 300, 300, 300, 500, 500, 500]
'''

# EVENTS_INDX TELLS YOU THE CURRENT EVENT YOUR ON
events_indx = 0

# IF YOU CHANGE THE 100 HERE, CHANGE THE CODE IN RAIN PARTICLES. IT IS CALLED TWICE IN PARTICLE_EMITTER.PY
# UNCOMMENT IN DRAW FOR PARTICLE_EMITTER.PY
#player.emitter.rain_particles(200)

while True:
    # CYCLE THROUGH FRAME_LIST EVERY 1000 MS
    # _________________________________________________________________________________________________________________________
    curr_time = pygame.time.get_ticks()
    if next_frame_time - curr_time < 0:
        next_frame_time = curr_time + events_times[current_frame]
        
        if current_frame in transit_frames:
            events_indx += 1 

        current_frame = current_frame + 1
        if events[events_indx][0] <= current_frame <= events[events_indx][1]:
            curr_map = frame_list[current_frame]
        else:
            current_frame = events[events_indx][0]
            curr_map = frame_list[current_frame]
    # _________________________________________________________________________________________________________________________


    #startTrackMalloc()
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
            if key == pygame.K_SPACE:
                pass
                #player.build(curr_map.tiles)

            # HANDLE ZOOMING
            # _________________________________________________________________________________________________________________________
            elif key == pygame.K_EQUALS:
                camera.zoom = min(camera.zoom + 1, 22)

            elif key == pygame.K_MINUS:
                camera.zoom = max(camera.zoom - 1, 6)
            # _________________________________________________________________________________________________________________________
            
            elif key == pygame.K_p:
                player.inMotion = True
                #player.shoot(curr_map.tiles, movingList)

            # (MANUALLY) MOVE TO THE NEXT FRAME
            elif key == pygame.K_n:
                events_indx += 1

            if not player.inMotion:
                wasdKeys(key, keys, player, curr_map)


    # Draw map and player
    # curr_map.draw(screen)
    camera.update(curr_map)
    camera.addE(player, screen)
    camera.addMap(0, curr_map)
    camera.renderMap(screen)

    for enemy in enemy_list:
        enemy.move(player, movingList, enemy_list, curr_map.tiles)
        #print(f"ENEMY POS X: {enemy.x}, POS Y: {enemy.y}")

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

                    sound = pygame.mixer.Sound("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/custom_hit_1.mp3")
                    sound.set_volume(0.05)  # Set volume to 30%
                    sound.play()  # Loop the sound indefinitely

                    ui.updateHealth(player.health)
                    movingList.remove(obj)
                    player.emitter.x = player.x
                    player.emitter.y = player.y
                    player.emitter.emit_particles_circular(player.x, player.y, 3)
                    continue

        for enemy in enemy_list:
            if obj.rect.colliderect(enemy.rect):
                if obj.team != "enemy":
                    time_delta = checkTime(enemy.next_hit, enemy.hit_cooldown)
                    if time_delta != -1:
                        enemy.health -= 1
                        enemy.next_hit = time_delta

                        sound = pygame.mixer.Sound("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/custom_hit_1.mp3")
                        sound.set_volume(0.05)  # Set volume to 30%
                        sound.play()  # Loop the sound indefinitely

                        if enemy.health == 0:
                            enemy_list.remove(enemy)
                        movingList.remove(obj)
                        enemy.emitter.x = enemy.x
                        enemy.emitter.y = enemy.y
                        enemy.emitter.emit_particles_circular(enemy.x, enemy.y, 2)
                        # Dont double free the same object
                        brake = 1
                        break

        if brake:
            continue

        if obj.move(curr_map) == -1:
            curr_time = pygame.time.get_ticks()
            if curr_time > obj.delete_time:
                movingList.remove(obj)
    
    for enemy in enemy_list:
        enemy.updateD(movingList)
        camera.addE(enemy, screen)

    camera.renderObj(screen)
    ui.heart_arr.draw(screen)
    ui.tool_bar.draw(screen)
    ui.minimap.draw(screen)

    player.updateD(screen, curr_map.tiles, movingList)
    player.emitter.update(camera.anchor, camera.gimble)
    player.emitter.draw(screen, camera)
    
    for enemy in enemy_list:
        enemy.emitter.update(camera.anchor, camera.gimble)
        enemy.emitter.draw(screen, camera)

    pygame.display.flip()
    clock.tick(60)

    #endTrackMalloc()