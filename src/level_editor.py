# IMPORTANT NOTE, WE USE BOTH IMAGE NAME AND THE REGULAR IMAGE BECAUSE IMAGE NAME IS EASILY SAVED IN AND READ FROM A FILE. 

import pygame
import sys

from global_functions import *
from cursor import Cursor
from mapy import Map
from cursor_cam import CursorCamera
from brush import Brush
from brush import UndoFrame
from side_bar import SideBar, LeftBar

import glob

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Landscape")


num_map_txts = len(glob.glob(MAP_TXT.format('*')))

#print(f"NUM: {num_map_txts}")

# CHECK IF ANY MAP FILES EXIST ALREADY
if num_map_txts == 0:
    frame_list.append(Map(TILE_SIZE, MAP_SIZE))

    # IF NO MAP FILES EXIST, INITIALIZE A GREEN MAP
    for i in range(MAP_RC[1]):
        for j in range(MAP_RC[0]):
                if TILE_SIZE == 10:
                    frame_list[0].tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/ground_10.png")
                    frame_list[0].tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/ground_10.png"
                    frame_list[0].tiles[i][j].walkable = True

                elif TILE_SIZE == 16: 
                    frame_list[0].tiles[i][j].image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_16/ground_16.png")
                    frame_list[0].tiles[i][j].name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_16/ground_16.png"
                    frame_list[0].tiles[i][j].walkable = True

    save()

# IF MAP FILES EXIST, LOAD THEM
else:
    for i in range(num_map_txts):
        print(f"load: {i}")
        frame_list.append(Map(TILE_SIZE, MAP_SIZE))
        frame_list[i].load(MAP_TXT.format(i))
        #print(f"WHAT DO YOU WANT TO BE? {len(frame_list[i].effects)}")

#print("Entering Sort Effects In Level Editor")
#frame_list[0].sortEffects()


# NOTE HAVE A CURRENT EFFECTS VAR?
curr_map = frame_list[current_frame]

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
leftbar = LeftBar()

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



'''
tracemalloc.start()
poll_mem_time = pygame.time.get_ticks() + 5000
global_mem_time_tracker = 0
'''

print(f"Height: {HEIGHT}")


while True: 

    # POLL MEM EVERY SECOND
    # _________________________________________________________________________________________________________________________
    '''
    curr_time = pygame.time.get_ticks()
    if poll_mem_time - curr_time < 0:
        global_mem_time_tracker += 1
        print()
        print(f"Mem Poll Number {global_mem_time_tracker}")
        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics('lineno')
        print("Top 10 memory usage lines:")
        for stat in stats[:10]:
            print(stat)
        poll_mem_time = curr_time + 5000
    '''
    # _________________________________________________________________________________________________________________________

    # CYCLE THROUGH FRAME_LIST EVERY 500 MS
    # _________________________________________________________________________________________________________________________
    if leftbar.play_state:
        curr_time = pygame.time.get_ticks()
        if next_frame_time - curr_time < 0:
            next_frame_time = curr_time + 500

            current_frame = (current_frame + 1) % len(frame_list)
            curr_map = frame_list[current_frame]
    # _________________________________________________________________________________________________________________________

    camera.update(mouse_pos)

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
                    
                    #print(f"draw effects: {sidebar.draw_effects}")
                    print("bef hanndle click")
                    sidebar.handleClick(mouse_pos, brush, current_frame, frame_list)
                    print("after handle click")
                    #print(f"draw effects: {sidebar.draw_effects}")
                    
                elif leftbar.visible and mouse_pos[0] < 100 and 138 < mouse_pos[1] < 100 + (leftbar.num_imgs * 75) + 50:
                    
                    mouse_pos = pygame.mouse.get_pos()
                    print("heresdfsdfsdfsfddfs\nfdgdfg")
                    # CAREFUL, LEFT BAR IS ALTERING GLOBAL STATE FOR SIDEBAR.DRAW EFFECTS BEWARE
                    current_frame = leftbar.handleClick(mouse_pos, brush, current_frame, frame_list, sidebar)
                    # IN CASE LEFT BAR ADDED A TILE, REFRESH SIDEBAR
                    if not leftbar.show_music:
                        sidebar.load_tile_imgs(f"*_{TILE_SIZE}.png")
                    else: 
                        sidebar.load_tile_imgs(f"*.mp3")
                    curr_map = frame_list[current_frame]

                elif brush.mode == "line":
                    brush.spec_x, brush.spec_y = [camera.coord[1], camera.coord[0]]
                
                else:
                    # THE REASON THIS CODE APEARS UNDER BOTH GET_PRESSED AND EVENT.BUTTON IS BECAUSE THERE ARE SOME CLICKS WHICH AREN'T LONG ENOUGH FOR A HOLD, BUT SHOULD DRAW SOMETHING ON THE SCREEN
                    brush.update(camera.coord[1], camera.coord[0])
                    
                    # WHATS PASSED INTO BRUSH.DRAW IS DIFFERENT DEPENDING ON IF YOU ARE DRAWING EFFECTS
                    if sidebar.draw_effects:
                        brush.draw(undo_stack, curr_map.transparent, sidebar.draw_effects)
                    else:
                        brush.draw(undo_stack, curr_map.tiles, sidebar.draw_effects)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pass

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0] and not(sidebar.visible and mouse_pos[0] > WIDTH - 200) and not(leftbar.visible and mouse_pos[0] < 100 and 138 < mouse_pos[1] < 475 + 138): # LEFT CLICK
                brush.update(camera.coord[1], camera.coord[0])

                # WHATS PASSED INTO BRUSH.DRAW IS DIFFERENT DEPENDING ON IF YOU ARE DRAWING EFFECTS
                if sidebar.draw_effects:
                    brush.draw(undo_stack, curr_map.transparent, sidebar.draw_effects)
                else:
                    brush.draw(undo_stack, curr_map.tiles, sidebar.draw_effects)

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
                brush.colorPicker(camera.coord[1], camera.coord[0], curr_map, sidebar)

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
            
            if event.key == pygame.K_MINUS:
                leftbar.visible = not leftbar.visible

            # TODO FIX THIS SHIT. ITS SO ASS IT HURTS
            # HANDLES REDO AND UNDO
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_z:
                if len(undo_stack) == 0: 
                    pass
                    #print("Nothing to undo")
                else:
                    #print("Undid")
                    '''
                    new_version = undo_stack.pop()

                    # REDO CODE FOR WHEN YOU UNDO
                    # _________________________________________________________________________________________________________________________
                    redo_version_name_arr, redo_version_img_arr = copyRect(new_version.x, new_version.y, new_version.brush_size, curr_map)
                    redo_version = UndoFrame(new_version.x, new_version.y, new_version.brush_size, redo_version_img_arr, redo_version_name_arr)
                    redo_stack.append(redo_version)
                    # _________________________________________________________________________________________________________________________
                    drawRectArr(new_version.x, new_version.y, new_version.brush_size, new_version.img_arr, new_version.name_arr, curr_map)
                    '''

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
    # The BRUSH IS A PARAMETER HERE BECAUSE THIS FUNCTION DRAWS WHERE THE CURSOR IS CURRENTLY AT AND SO IT USES THE BRUSH SIZE TO DRAW IT CORRECTLY

    #startTrackMalloc()

    #gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
    '''
    s_1 = tracemalloc.take_snapshot()
    
    print()
    print("JOE START")
    '''
    camera.addMap(curr_map, brush.size)

    camera.renderMap(curr_map, screen, brush.size)
    '''
    s_2 = tracemalloc.take_snapshot()

    top_stats = s_2.compare_to(s_1, 'lineno')

    print("lookup")
    for stat in top_stats[:10]:
        print("s: ", stat)
    print("done")
    '''
    """
    gc.collect()

    print("Top 10 memory allocations:\n")
    
    print("dope:", gc.garbage)

    for obj in gc.garbage:
        print(f"Uncollectable object: {obj}")
        print(f"Type: {type(obj)}")
        print(f"Refs: {gc.get_referrers(obj)}")
        print(f"Attributes: {obj.__dict__ if hasattr(obj, '__dict__') else 'No __dict__'}")

    print()

    #print("Collected objects:", gc.garbage)

    gc.set_debug(0)

    print("JOE OVER")
    print()
    """

    #endTrackMalloc()

    if sidebar.visible:
        sidebar.show(screen)
        
        if leftbar.show_music:
            sidebar.text_group.update()
            sidebar.text_group.draw(screen)



    if leftbar.visible:
        #print("INNNN")
        leftbar.show(screen)

    camera.renderObj(screen)

    pygame.display.flip()
    clock.tick(60)