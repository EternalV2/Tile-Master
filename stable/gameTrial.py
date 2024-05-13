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

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Landscape")

ui = UserI(3)

# Create objects
gameMap = Map(WIDTH, HEIGHT, TILE_SIZE)
player = Player(100, 100, 5, 35)

# Main game loop
clock = pygame.time.Clock()

movingList = []

# Dictionary to store key states and timers
key_states = {}
key_start_times = {}

enemy_list = []
for i in range(3):
    enemy_list.append(Enemy((150 * i) + 1000, 150 * i + 300, TILE_SIZE, 35))

enemy_list.append(Enemy(700,  700, TILE_SIZE, 35))
enemy_list.append(Enemy(650,  700, TILE_SIZE, 35))
enemy_list.append(Enemy(600,  700, TILE_SIZE, 35))


enemy_list.append(Enemy(750,  700, TILE_SIZE, 35))
enemy_list.append(Enemy(800,  700, TILE_SIZE, 35))

enemy_list.append(Enemy(850,  700, TILE_SIZE, 35))

enemy_list.append(Enemy(900,  700, TILE_SIZE, 35))
'''
enemy_list.append(Enemy(700,  600, TILE_SIZE, 35))

enemy_list.append(Enemy(650,  600, TILE_SIZE, 35))
enemy_list.append(Enemy(600,  600, TILE_SIZE, 35))

enemy_list.append(Enemy(750,  600, TILE_SIZE, 35))
enemy_list.append(Enemy(800,  600, TILE_SIZE, 35))
enemy_list.append(Enemy(850,  600, TILE_SIZE, 35))
enemy_list.append(Enemy(900,  600, TILE_SIZE, 35))
'''

while True:
    sprite_group = pygame.sprite.Group()

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
                player.build(gameMap.tiles)

            elif key == pygame.K_p:
                player.shoot(gameMap.tiles, movingList)

    sprite_group.add(player)

    screen.fill((255, 255, 255))

    # Draw map and player
    gameMap.draw(screen)

    for enemy in enemy_list:
        enemy.move(player, movingList, enemy_list, gameMap.tiles)
        sprite_group.add(enemy)

    for obj in movingList:
        sprite_group.add(obj)

        brake = 0

        #Attach emitter to player and Enemies

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
                        #Dont double free the same object
                        brake = 1
                        break 
        
        if brake:
            continue

        obj.emitter.update()
        obj.emitter.draw(screen)


        if obj.move() == -1:
            curr_time = pygame.time.get_ticks()
            if curr_time > obj.delete_time:
                movingList.remove(obj)
                

    sprite_group.update()
    sprite_group.draw(screen)
    ui.heart_arr.draw(screen)

    player.updateD(movingList)
    player.emitter.update()
    player.emitter.draw(screen)

    for enemy in enemy_list:
        enemy.updateD(movingList)
        enemy.emitter.update()
        enemy.emitter.draw(screen)

    pygame.display.flip()
    clock.tick(60)
