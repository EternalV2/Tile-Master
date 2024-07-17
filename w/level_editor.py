# IMPORTANT NOTE, WE USE BOTH IMAGE NAME AND THE REGULAR IMAGE BECAUSE IMAGE NAME IS EASILY SAVED IN AND READ FROM A FILE. 

import pygame
import sys

from global_functions import *
from cursor import Cursor
from mapy import Map
from cursor_cam import CursorCamera
from brush import Brush
from brush import UndoFrame
from side_bar import SideBar
import glob

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Landscape")


num_map_txts = len(glob.glob(MAP_TXT.format('*')))

frame_list = []
current_frame = 0

for i in range(num_map_txts):
    frame_list.append(Map(TILE_SIZE, MAP_SIZE))
    frame_list[i].load(MAP_TXT.format(i))

curr_map = frame_list[current_frame]

'''
for i in range(len(map_2.tiles)):
    for j in range((len(map_2.tiles[0]))):
        if j == 50: 
            map_2.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png")
            map_2.tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png"
            map_2.tiles[i][j].walkable = True
        else: 
            map_2.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")
            map_2.tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png"
            map_2.tiles[i][j].walkable = True

for i in range(len(map_2.tiles)):
    if i % 3 == 0:
        map_2.tiles[i][55].walkable = False
        map_2.tiles[i][55].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png")
        map_2.tiles[i][55].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png"
'''

cursor = Cursor(ORI_MOUSE_POS[0], ORI_MOUSE_POS[1])
pygame.mouse.set_pos((ORI_MOUSE_POS[0], ORI_MOUSE_POS[1]))

camera = CursorCamera(cursor)

# Main game loop
clock = pygame.time.Clock()

key_states = {}
key_start_times = {}

brush = Brush(0, 0)

undo_stack = []
redo_stack = []

sidebar = SideBar()

def save():

    name_walkable_mapping = {}

    # DIVE INTO TILE_LOG.TXT TO MATCH THE IMAGE NAME WITH THE IS_WALKABLE AND IMG_TILE_SIZE ATTRIBUTES
    # I PUT TILE_SIZE INTO THE TXT DOCUMENT BECAUSE WE MIGHT NEED IT BUT RIGHT NOW ITS NOT BEING USED
    with open(TILE_LOG_TXT, 'r') as file: 
        for line in file:
            parts = line.strip().split(', ')
            name_walkable_mapping[parts[2]] = True if parts[1] == "True" else False

    for i in range(len(frame_list)):
        print(f"TOBEY {i}")
        data = [[None for _ in range(MAP_RC[0])] for _ in range(MAP_RC[1])]

        for row in range(len(frame_list[i].tiles)):
            for col in range(len(frame_list[i].tiles[0])):
                # ACCESS PREVIOUSLY MADE HASHMAP TO SEE IF TILE IS_WALKABLE
                is_walkable_temp = name_walkable_mapping[frame_list[i].tiles[row][col].name]

                data[row][col] = frame_list[i].tiles[row][col].write_tile(is_walkable_temp)

        save_string = '\n'.join([','.join(sub_array) for sub_array in data])

        with open(MAP_TXT.format(i), 'w') as file:
            # Write data to the file
            file.write(save_string)

def wasdKeys2(key, keys):
    # Implement actions based on held keys
    if key == pygame.K_a:

        if keys[pygame.K_a] and keys[pygame.K_w]:
            camera.wasd_pan = [camera.wasd_pan[0] - 1, camera.wasd_pan[1] - 1]
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            camera.wasd_pan = [camera.wasd_pan[0] - 1, camera.wasd_pan[1] + 1]
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            return
        else:
            camera.wasd_pan = [camera.wasd_pan[0] - 1, camera.wasd_pan[1]]

    elif key == pygame.K_d:

        if keys[pygame.K_d] and keys[pygame.K_w]:
            camera.wasd_pan = [camera.wasd_pan[0] + 1, camera.wasd_pan[1] - 1]
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            camera.wasd_pan = [camera.wasd_pan[0] + 1, camera.wasd_pan[1] + 1]
        elif keys[pygame.K_d] and keys[pygame.K_a]:
            return
        else:
            camera.wasd_pan = [camera.wasd_pan[0] + 1, camera.wasd_pan[1]]

    elif key == pygame.K_w:

        if keys[pygame.K_w] and keys[pygame.K_a]:
            camera.wasd_pan = [camera.wasd_pan[0] - 1, camera.wasd_pan[1] - 1]
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            camera.wasd_pan = [camera.wasd_pan[0] + 1, camera.wasd_pan[1] - 1]
        elif keys[pygame.K_w] and keys[pygame.K_s]:
            return
        else:
            camera.wasd_pan = [camera.wasd_pan[0], camera.wasd_pan[1] - 1]

    elif key == pygame.K_s:

        if keys[pygame.K_s] and keys[pygame.K_a]:
            camera.wasd_pan = [camera.wasd_pan[0] - 1, camera.wasd_pan[1] + 1]
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            camera.wasd_pan = [camera.wasd_pan[0] + 1, camera.wasd_pan[1] + 1]
        elif keys[pygame.K_s] and keys[pygame.K_w]:
            return
        else:
            camera.wasd_pan = [camera.wasd_pan[0], camera.wasd_pan[1] + 1]
            
mouse_pos = [0, 0]

# GET CURRENT_TIME + 500 MS 
next_frame_time = pygame.time.get_ticks() + 500

while True: 
    if sidebar.play_state:
        
        curr_time = pygame.time.get_ticks()
        if next_frame_time - curr_time < 0:
            next_frame_time = curr_time + 500

            current_frame = (current_frame + 1) % len(frame_list)
            curr_map = frame_list[current_frame]

    camera.update(curr_map, mouse_pos)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                pass

            # THIS SHOULD ONLY REGISTER INDIVIDUAL CLICKS USE MOUSE.GET_PRESSED()[0] FOR REGISTERING HOLDS
            if event.button == 1: 
                if sidebar.visible and mouse_pos[0] > WIDTH - 200:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    current_frame = sidebar.handleClick(mouse_pos, brush, current_frame, frame_list)
                    print(f"current frame: {current_frame}")
                    curr_map = frame_list[current_frame]
                    
                    #print(f"brush.is_walkable after handle click call: {brush.is_walkable}")
                    #print("BNAME", brush.name)
                elif brush.mode == "line":
                    brush.spec_x, brush.spec_y = [camera.coord[1], camera.coord[0]]
                
                else:
                    # THE REASON THIS CODE APEARS UNDER BOTH GET_PRESSED AND EVENT.BUTTON IS BECAUSE THERE ARE SOME CLICKS WHICH AREN'T REGISTER ENOUGH FOR A HOLD, BUT SHOULD DRAW SOMETHING ON THE SCREEN
                    # DONT PUSH ALL MAP ONTO STACK. PUSH ONLY CHANGED PARTS
                    brush.update(camera.coord[1], camera.coord[0])
                    brush.draw(undo_stack, curr_map)
                    #print("gameMap 0 0: ", gameMap.tiles[0][0].name)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pass

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0] and not(sidebar.visible and mouse_pos[0] > WIDTH - 200): # LEFT CLICK
                brush.update(camera.coord[1], camera.coord[0])
                brush.draw(undo_stack, curr_map)
                #print("gameMap 0 0: ", gameMap.tiles[0][0].name)

    # KEYS 
    # _________________________________________________________________________________________________________________________
        elif event.type == pygame.KEYDOWN:

            # REGISTER INDIVIDUAL KEY PRESSES
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_e:
                brush.resizeUp()
        
            if event.key == pygame.K_q:
                brush.resizeDown()

            if event.key == pygame.K_o:
                brush.colorPicker(camera.coord[1], camera.coord[0], curr_map)

            # HANDLES SCROLLING THE SIDEBAR (SHOULD BE DIFFERENT FROM PANNING THE MAP)
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_w:
                if sidebar.visible: 
                    sidebar.scroll_offset -= 1

            if event.key == pygame.K_s:
                if sidebar.visible: 
                    sidebar.scroll_offset += 1
            # _________________________________________________________________________________________________________________________

            if event.key == pygame.K_EQUALS:
                #print(f"HAMILTON")
                sidebar.visible = not sidebar.visible

            # TODO FIX THIS SHIT. ITS SO ASS IT HURTS
            # HANDLES REDO AND UNDO
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_z:
                if len(undo_stack) == 0: 
                    pass
                    #print("Nothing to undo")
                else:
                    #print("Undid")
                    new_version = undo_stack.pop()

                    # REDO CODE FOR WHEN YOU UNDO
                    # _________________________________________________________________________________________________________________________
                    redo_version_name_arr, redo_version_img_arr = copyRect(new_version.x, new_version.y, new_version.brush_size, curr_map)
                    redo_version = UndoFrame(new_version.x, new_version.y, new_version.brush_size, redo_version_img_arr, redo_version_name_arr)
                    redo_stack.append(redo_version)
                    # _________________________________________________________________________________________________________________________
                    drawRectArr(new_version.x, new_version.y, new_version.brush_size, new_version.img_arr, new_version.name_arr, curr_map)

            if event.key == pygame.K_y:
                if len(redo_stack) == 0: 
                    pass
                    #print("Nothing to redo")
                else:
                    #print("redid")

                    new_version = redo_stack.pop()

                    # UNDO CODE FOR WHEN YOU REDO
                    # _________________________________________________________________________________________________________________________
                    undo_version_name_arr, undo_version_img_arr = copyRect(new_version.x, new_version.y, new_version.brush_size, curr_map)
                    undo_version = UndoFrame(new_version.x, new_version.y, new_version.brush_size, undo_version_img_arr, undo_version_name_arr)
                    undo_stack.append(undo_version)
                    # _________________________________________________________________________________________________________________________

                    drawRectArr(new_version.x, new_version.y, new_version.brush_size, new_version.img_arr, new_version.name_arr, curr_map)
            # _________________________________________________________________________________________________________________________
            # UNDO & REDO SECTION END

            if event.key == pygame.K_x:
                save()
            # _________________________________________________________________________________________________________________________
            # INDIVIDUAL KEY PRESS SECTION END

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
            # JUST TO MAKE THE SIDEBAR AND MAP NOT PAN AT THE SAME TIME
            if not sidebar.visible:
                wasdKeys2(key, keys)

            if key == pygame.K_l: 
                if not brush.mode == "line":
                    brush.mode = "line"
                else:
                    brush.mode = ""
                    
    #_________________________________________________________________________________________________________________________
    # The BRUSH IS A PARAMETER HERE BECAUSE THIS FUNCTION DRAWS WHERE THE CURSOR IS CURRENTLY AT AND SO IT USUES THE BRUSH SIZE TO DRAW IT CORRECTLY
    
    camera.addMap(0, curr_map, brush.size)
    camera.renderMap(screen, curr_map, brush.size)
    
    if sidebar.visible:
        sidebar.show(screen)

    camera.renderObj(screen)

    pygame.display.flip()
    clock.tick(60)