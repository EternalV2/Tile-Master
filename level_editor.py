import pygame
import sys

from global_functions import *
from cursor import Cursor
from mapy import Map
from cursor_cam import CursorCamera
from brush import Brush
from brush import UndoFrame
from side_bar import SideBar

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Landscape")

gameMap = Map(TILE_SIZE, MAP_SIZE)

for i in range(len(gameMap.tiles)):
    for j in range((len(gameMap.tiles[0]))):
        if j == 50: 
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png")
            gameMap.tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_1_10.png"
            gameMap.tiles[i][j].walkable = True
        else: 
            gameMap.tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")
            gameMap.tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png"
            gameMap.tiles[i][j].walkable = True

for i in range(len(gameMap.tiles)):
    if i % 3 == 0:
        gameMap.tiles[i][55].walkable = False
        gameMap.tiles[i][55].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png")
        gameMap.tiles[i][55].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png"

cursor = Cursor(ORI_MOUSE_POS[0], ORI_MOUSE_POS[1])
pygame.mouse.set_pos((ORI_MOUSE_POS[0], ORI_MOUSE_POS[1]))

camera = CursorCamera(cursor)

# Main game loop
clock = pygame.time.Clock()

key_states = {}
key_start_times = {}

brush = Brush(0, 0, gameMap)

undo_stack = []
redo_stack = []

sidebar = SideBar()

def save():
    data = [[None for _ in range(MAP_RC[0])] for _ in range(MAP_RC[1])]

    print("SPRIIT: ", gameMap.tiles[0][0].name)

    '''

    for row in range(len(full_map.tiles)):
        for col in range(len(full_map.tiles[0])):
            #print(f"R: {row} & LEN: {len(data)} || C: {col} & LEN: {len(data[0])}")
            data[row][col] = full_map.tiles[row][col].write_tile()

    save_string = '\n'.join([','.join(sub_array) for sub_array in data])


    print(MAP_TXT)

    with open(MAP_TXT, 'w') as file:
        # Write data to the file
        file.write(save_string)

    print("\n\n\n\n\n\n\n\n\nSAVED\n\n\n\n\n\n\n\n\n\n")

    '''


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

while True: 
    camera.update(gameMap, mouse_pos)

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
                    sidebar.handleClick(mouse_pos, brush)
                    print("BNAME", brush.name)
                elif brush.mode == "line":
                    brush.spec_x, brush.spec_y = [camera.coord[1], camera.coord[0]]
                
                else:
                    # THE REASON THIS CODE APEARS UNDER BOTH GET_PRESSED AND EVENT.BUTTON IS BECAUSE THERE ARE SOME CLICKS WHICH AREN'T REGISTER ENOUGH FOR A HOLD, BUT SHOULD DRAW SOMETHING ON THE SCREEN
                    # DONT PUSH ALL MAP ONTO STACK. PUSH ONLY CHANGED PARTS
                    brush.update(camera.coord[1], camera.coord[0])
                    brush.draw(undo_stack, gameMap)
                    print("HERE?", gameMap.tiles[0][0].name)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pass

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0] and not(sidebar.visible and mouse_pos[0] > WIDTH - 200): # LEFT CLICK
                brush.update(camera.coord[1], camera.coord[0])
                brush.draw(undo_stack, gameMap)
                print("HERE?", gameMap.tiles[0][0].name)

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
                brush.colorPicker(camera.coord[1], camera.coord[0], gameMap)

            if event.key == pygame.K_EQUALS:
                print(f"HAMILTON")
                sidebar.visible = not sidebar.visible

            # TODO FIX THIS SHIT. ITS SO ASS IT HURTS
            # HANDLES REDO AND UNDO
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_z:
                if len(undo_stack) == 0: 
                    print("Nothing to undo")
                else:
                    print("Undid")
                    new_version = undo_stack.pop()

                    # REDO CODE FOR WHEN YOU UNDO
                    # _________________________________________________________________________________________________________________________
                    redo_version_arr = copyRect(new_version.x, new_version.y, new_version.brush_size, gameMap)
                    redo_version = UndoFrame(new_version.x, new_version.y, new_version.brush_size, redo_version_arr)
                    redo_stack.append(redo_version)
                    # _________________________________________________________________________________________________________________________
                    drawRectArr(new_version.x, new_version.y, new_version.brush_size, new_version.img_arr, gameMap)

            if event.key == pygame.K_y:
                if len(redo_stack) == 0: 
                    print("Nothing to redo")
                else:
                    print("redid")

                    new_version = redo_stack.pop()

                    # UNDO CODE FOR WHEN YOU REDO
                    # _________________________________________________________________________________________________________________________
                    undo_version_arr = copyRect(new_version.x, new_version.y, new_version.brush_size, gameMap)
                    undo_version = UndoFrame(new_version.x, new_version.y, new_version.brush_size, undo_version_arr)
                    undo_stack.append(undo_version)
                    # _________________________________________________________________________________________________________________________

                    drawRectArr(new_version.x, new_version.y, new_version.brush_size, new_version.img_arr, gameMap)
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
            wasdKeys2(key, keys)

            if key == pygame.K_l: 
                if not brush.mode == "line":
                    brush.mode = "line"
                else:
                    brush.mode = ""
                    
    #_________________________________________________________________________________________________________________________
    # The BRUSH IS A PARAMETER HERE BECAUSE THIS FUNCTION DRAWS WHERE THE CURSOR IS CURRENTLY AT AND SO IT USUES THE BRUSH SIZE TO DRAW IT CORRECTLY
    camera.addMap(0, gameMap, brush.size)

    camera.renderMap(screen, gameMap, brush.size)

    if sidebar.visible:
        sidebar.show(screen)

    camera.renderObj(screen)

    pygame.display.flip()
    clock.tick(60)