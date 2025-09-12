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

num_map_txts = len(glob.glob(MAP_TXT.format('*')))

for i in range(num_map_txts):
    frame_list.append(Map(TILE_SIZE, MAP_SIZE))
    frame_list[i].load(MAP_TXT.format(i))

next_frame_time = pygame.time.get_ticks() + 1000

curr_map = frame_list[0]

aim = {'lu': (-3, -3), 'ld': (-3, 3), 'rd': (3, 3), 'ru': (3, -3), 'r': (4, 0), 'l': (-4, 0), 'd': (0, 4), 'u': (0, -4)}
player = Player(SPAWN[0], SPAWN[1], 5, "gandalf", aim, .35, False, 100, 20)
cursor = Cursor(ORI_MOUSE_POS[0], ORI_MOUSE_POS[1])
pygame.mouse.set_pos((ORI_MOUSE_POS[0], ORI_MOUSE_POS[1]))

# Main game loop
clock = pygame.time.Clock()

movingList = []

# Dictionary to store key states and timers
key_states = {}
key_start_times = {}

enemy_list = []

balrog_aim = {'lu': (-6, 3), 'ld': (-6, 3), 'rd': (5, 3), 'ru': (4, 2), 'r': (4, 2), 'l': (-7, 3), 'd': (0, 5), 'u': (0, -5)}
enemy_list.append(Npc(45, 6, TILE_SIZE, "enemy", "balrog", balrog_aim, .2, True, 35))

camera = Camera(player, TILE_SIZE)

# EVENTS IS THE RANGE OF FRAMES YOUR  CURRENTLY ON
# TRANSIT FRAMES ARE FRAMES WHICH ONLY PLAY ONCE
# EVENTS_TIMES ARE THE TIMES BETWEEN EACH FRAME
events = [[0, 2]]
transit_frames = []
events_times = [1000, 1000, 1000]

# EVENTS_INDX TELLS YOU THE CURRENT EVENT YOUR ON
events_indx = 0

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

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            cursor.x, cursor.y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE

        # BUILD KEY STATE LIST
        elif event.type == pygame.KEYDOWN:
            # Key is pressed down
            key_states[event.key] = True
            if event.key not in key_start_times:
                key_start_times[event.key] = pygame.time.get_ticks()

        elif event.type == pygame.KEYUP:
            # Key is released
            key_states[event.key] = False
            if event.key in key_start_times:
                del key_start_times[event.key]

    # Check for held keys and update timers
    for key, state in key_states.items():
        if state:
            # HANDLE ZOOMING
            # _________________________________________________________________________________________________________________________
            if key == pygame.K_EQUALS:
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


    camera.update(curr_map)
    camera.addE(player, screen)
    camera.addMap(0, curr_map)
    camera.renderMap(screen)

    for enemy in enemy_list:
        enemy.move(player, movingList, enemy_list, curr_map.tiles)

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
                    sound.set_volume(0.05)
                    sound.play()

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
                        sound.set_volume(0.05)
                        sound.play()

                        if enemy.health == 0:
                            enemy_list.remove(enemy)
                        movingList.remove(obj)
                        enemy.emitter.x = enemy.x
                        enemy.emitter.y = enemy.y
                        enemy.emitter.emit_particles_circular(enemy.x, enemy.y, 2)

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
