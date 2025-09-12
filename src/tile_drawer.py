import pygame
import os
import glob
import sys

from PIL import Image
from global_functions import *
from button import Button

# TODO GETTING ERROR WHEN WE EXIT OUT OF TILE_DRAWER

pygame.init()

# THIS IS USED SOLELY TO NAME THE OUTPUT IMAGES
# _________________________________________________________________________________________________________________________
if TILE_SIZE == 10:
    pattern = os.path.join("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/" + MAP_NAME + f"/_10", "*_10.png")
elif TILE_SIZE == 16: 
    pattern = os.path.join("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/" + MAP_NAME + f"/_16", "*_16.png")
elif TILE_SIZE == 32:
    pattern = os.path.join("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/" + MAP_NAME + f"/_32", "*_32.png")
tile_imgs = glob.glob(pattern)
#print(f"pls pls pls {pattern}")
num_imgs = len(tile_imgs)
# _________________________________________________________________________________________________________________________

# THIS IS IMPORTANT FOR THE HOVERING COLLISION DETECTION & THE DRAWING
RED_BAR_HEIGHT = 25

# RANDOM VALUES, THOUGHT THEY LOOKED GOOD
width, height = 820, 500

# REGULAR PYGAME WINDOW INITIALIZATION
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")
clock = pygame.time.Clock()

brush_size = 1

prev_colors = []
prev_pos = [None, None]

# 10 X 10 PIXEL GRID WHICH IS BASIS FOR PNG IMAGE
canvas_grid = [[(255, 255, 255, 0) for _ in range(TILE_SIZE)] for _ in range(TILE_SIZE)]

# SETS THE DEFAULT BRUSH COLOR TO BLACK
current_color = (0, 0, 0)

# THIS IS THE VALUE GIVEN BY HOVERING OVER THE RED SLIDER
red_offset = 0

# THIS IS THE NEXT TIME YOU SHOULD CHECK WHETHER THE MOUSE IS HOVERING OVER THE RED SLIDER
poll_red_bar = 1

# THIS TOGLES WHETHER YOU SHOW THE GRID LINES (PRESS "G" TO TURN ON OR OFF)
show_gridlines = True



# INITIALIZE THE FONTS
# _________________________________________________________________________________________________________________________
font = pygame.font.Font(None, 32)
save_text_box = pygame.Rect(530, 360+75, 140, 32)
save_text = ""
save_active = False
save_color_inactive = pygame.Color('lightskyblue3')
save_color_active = pygame.Color('dodgerblue2')
save_curr_color = save_color_inactive
# _________________________________________________________________________________________________________________________



button_group = pygame.sprite.Group()

# BELOW SECTION HANDLES THE SET_WALKABLE BUTTON
# _________________________________________________________________________________________________________________________
# INITIALIZE THE "SET WALKABLE BUTTON" (SLIGHT TO THE LEFT OF THE CURRENT BRUSH TILE)
# WALKABLE_IMAGE SHOULD NOT BE ACCESED DIRECTLY AFTER CREATING THE BUTTON. I DONT THINK THAT WOULD MAKE SENSE
# CREATE BOTH BUTTONS AT STARTUP AND ALTERNATE THE DISPLAY BETWEEN THEM USING THE SETWALKABLE_BUTTON POINTER BASICALLY
blue_walkable_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/blue_walkable_10_special.png"
blue_walkable_image = pygame.image.load(blue_walkable_image_name)

red_walkable_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_walkable_10_special.png"
red_walkable_image = pygame.image.load(red_walkable_image_name)

blue_walkable_button = Button(530, 360 - 25, 50, blue_walkable_image, pygame.transform.scale(blue_walkable_image, (50, 50)), blue_walkable_image_name)
red_walkable_button = Button(530, 360 - 25, 50, red_walkable_image, pygame.transform.scale(red_walkable_image, (50, 50)), red_walkable_image_name)

# DEFAULT IS_ WALKABLE = TRUE SO SET WALKABLE BUTTON WILL BE RED (TO TURN IT OFF)
set_walkable_button = red_walkable_button

# TOGGLES WHETHER THE TILE BEING CREATED IS WALKABLE
is_walkable = True
tile_transparent = False
button_group.add(set_walkable_button)
# _________________________________________________________________________________________________________________________



# _________________________________________________________________________________________________________________________
blue_t_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/blue_t_10_special.png"
blue_t_image = pygame.image.load(blue_t_image_name)

red_t_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_t_10_special.png"
red_t_image = pygame.image.load(red_t_image_name)

blue_t_button = Button(786 - 50, 360 - 25, 50, blue_t_image, pygame.transform.scale(blue_t_image, (50, 50)), blue_t_image_name)
red_t_button = Button(786 - 50, 360 - 25, 50, red_t_image, pygame.transform.scale(red_t_image, (50, 50)), red_t_image_name)

# DEFAULT IS_ WALKABLE = FALSE SO SET TRANSPARENT BUTTON WILL BE BLUE (TO TURN IT ON)
set_t_button = blue_t_button

# TOGGLES WHETHER THE TILE BEING CREATED IS WALKABLE
px_transparent = False

button_group.add(set_t_button)

spacing = (500 // TILE_SIZE)
# _________________________________________________________________________________________________________________________


#print("welcome to tile drawer!")
#print(f"crap {num_imgs}")

def save(img_name):
    is_transparent = False
    for row in range(len(canvas_grid)):
        for col in range(len(canvas_grid[0])):
            if canvas_grid[row][col] == (255, 255, 255, 0):
                is_transparent = True
                break
        if is_transparent:
            break                

    with open(TILE_LOG_TXT, 'a') as file:
        # Write text to the file
        file.write(f"{TILE_SIZE}, {is_walkable}, {is_transparent}, {img_name}\n")

    lines = []
    with open(TILE_LOG_TXT, 'r') as file:
        lines = file.readlines()

    lines = reversed(lines)
    saved_lines = []

    seen = set()

    for line in lines:
        parts = line.strip().split(', ')
        if parts[3] not in seen:
            seen.add(parts[3])
            saved_lines.append(line)
    
    saved_lines = reversed(saved_lines)

    with open(TILE_LOG_TXT, 'w') as file:
        for line in saved_lines:
            file.write(line)

while True:         
    # USE THE RED BAR, EVEN IF YOU DONT CLICK (ALLOWS HOVERING)
    # _________________________________________________________________________________________________________________________
    time_delta = checkTime(poll_red_bar, 50)
    if time_delta != -1: 
        mouse_pos = pygame.mouse.get_pos()
        poll_red_bar = time_delta

        if 530 < mouse_pos[0] < 530 + 256 and 330 < mouse_pos[1] < 330 + RED_BAR_HEIGHT: 
            red_offset = mouse_pos[0] - 530
    # _________________________________________________________________________________________________________________________

    # REGULAR PYGAME QUIT CODE
    # _________________________________________________________________________________________________________________________
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # _________________________________________________________________________________________________________________________

        # SEE IF LEFT CLICK IS HELD
        if pygame.mouse.get_pressed()[0]:
            
            # GET THE POSITION OF THE MOUSE
            mouse_pos = pygame.mouse.get_pos()
            
            # MAKE A RECT OF IT FOR COLLISION DETECTION WITH BUTTONS
            # _________________________________________________________________________________________________________________________

            # _________________________________________________________________________________________________________________________
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
            if mouse_rect.colliderect(set_walkable_button): 
                is_walkable = not is_walkable
                if set_walkable_button == blue_walkable_button:
                    set_walkable_button = red_walkable_button
                else:
                    set_walkable_button = blue_walkable_button
                button_group.empty()
                button_group.add(set_walkable_button)
                button_group.add(set_t_button)

            if mouse_rect.colliderect(set_t_button): 
                px_transparent = not px_transparent
                if set_t_button == blue_t_button:
                    set_t_button = red_t_button
                else:
                    set_t_button = blue_t_button
                button_group.empty()
                button_group.add(set_walkable_button)
                button_group.add(set_t_button)
            # _________________________________________________________________________________________________________________________

            if mouse_rect.colliderect(save_text_box):
                save_active = not save_active
                
            else:
                save_active = False

            save_curr_color = save_color_active if save_active else save_color_inactive

            # PICK COLOR (BOUNDARY CHECKS ARE FOR BLUE-GREEN GRID)
            # _________________________________________________________________________________________________________________________
            if 530 < mouse_pos[0] < 530 + 256 and 300 - 256 < mouse_pos[1] < 300: 
                #print(f"x: {mouse_pos[0]} y: {mouse_pos[1]} gr: {mouse_pos[0] - 530} bl: {mouse_pos[1] - (300 - 256)}")
                
                blue_offset = mouse_pos[0] - 530
                green_offset = mouse_pos[1] - (300 - 256)

                current_color = (red_offset, blue_offset, 256 - green_offset, 255)
            # _________________________________________________________________________________________________________________________

            # CHECK IF MOUSE IS ON CANVAS. IF IT IS, DRAW (THE 50'S HERE ARE JUST SPACE ALLOCATED FOR CANVAS DIVIDED BY NUMBER OF PIXELS)
            elif 0 < mouse_pos[0] < spacing * TILE_SIZE and mouse_pos[1] < spacing * TILE_SIZE:
                x, y = mouse_pos[0] // spacing, mouse_pos[1] // spacing
                
                start_row, end_row = max(0, x - brush_size + 1), min(TILE_SIZE, x + brush_size)
                start_col, end_col = max(0, y - brush_size + 1), min(TILE_SIZE, y + brush_size)

                if px_transparent: 
                    for row in range(start_row, end_row, 1):
                        for col in range(start_col, end_col, 1):
                            canvas_grid[row][col] = (255, 255, 255, 0)
                else:
                    for row in range(start_row, end_row, 1):
                        for col in range(start_col, end_col, 1):
                            canvas_grid[row][col] = current_color

        elif event.type == pygame.KEYDOWN:
            # TOGGLE IF THE GRID LINES ARE VISIBLE
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_g: 
                if not save_active:
                    show_gridlines = not show_gridlines
            # _________________________________________________________________________________________________________________________

            # SAVE AS PNG
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_x: 
                if not save_active:
                    image = Image.new("RGBA", (TILE_SIZE, TILE_SIZE))
                    pixels = image.load()
                    for i in range(TILE_SIZE):
                        for j in range(TILE_SIZE):
                            #print(f"{canvas_grid[i][j]}")
                            pixels[i, j] = canvas_grid[i][j]

                    if save_text == "":
                        img_name = f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_{TILE_SIZE}/output_image_{num_imgs}_{TILE_SIZE}.png"
                    else:
                        img_name = f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_{TILE_SIZE}/{save_text}_{TILE_SIZE}.png"

                    image.save(img_name)
                    save(img_name)
                    print("Image saved as {img_name}.png")
                    num_imgs += 1
            # _________________________________________________________________________________________________________________________

            # GET COLOR OF PIXEL THE MOUSE IS OVER
            # _________________________________________________________________________________________________________________________
            elif event.key == pygame.K_o: 
                mouse_pos = pygame.mouse.get_pos()
                if 0 < mouse_pos[0] < spacing * TILE_SIZE and mouse_pos[1] < spacing * TILE_SIZE:
                    current_color = canvas_grid[mouse_pos[0] // 31][mouse_pos[1] // 31]
            # _________________________________________________________________________________________________________________________

            if event.key == pygame.K_e: 
                brush_size = min(brush_size + 1, 4)
            
            if event.key == pygame.K_q: 
                brush_size = max(brush_size - 1, 1)

            if save_active:
                if event.key == pygame.K_RETURN:
                    #print(save_text)
                    save_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    save_text = save_text[:-1]
                else:
                    save_text += event.unicode

    # Fill the window with a color (optional, for example, white)
    window.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos[0] // spacing, mouse_pos[1] // spacing
    start_row, end_row = max(0, x - brush_size + 1), min(TILE_SIZE, x + brush_size)
    start_col, end_col = max(0, y - brush_size + 1), min(TILE_SIZE, y + brush_size)

    # PRINT CANVAS
    for i in range(len(canvas_grid)):
        for j in range(len(canvas_grid[0])):
            if start_row <= i < end_row and start_col <= j < end_col:
                pygame.draw.rect(window, [117, 117, 117, 0], (i * (spacing), j * (spacing), spacing, spacing))
            else:
                pygame.draw.rect(window, canvas_grid[i][j], (i * (spacing), j * (spacing), spacing, spacing))

    

    # PRINT GRIDLINES
    if show_gridlines: 
        for i in range(len(canvas_grid)):
            for j in range(len(canvas_grid[0])):
                pygame.draw.rect(window, (0, 0, 0), (i * (spacing), j * (spacing), spacing, spacing), 2)

    # PRINT RED BAR
    for i in range(256):
            pygame.draw.rect(window, (i, 0, 0), (530 + i, 300 + 30, 1, RED_BAR_HEIGHT))
    
    # PRINT GREEN-BLUE GRID
    for i in range(256):
        for j in range(256):
            pygame.draw.rect(window, (red_offset, i, j), (530 + i, 300 - j, 1, 1))

    # PRINT THE CURRENT COLOR OF THE BRUSH ON THE RIGHT PANEL
    pygame.draw.rect(window, current_color, (645, 300 + 60, spacing, spacing))

    # DRAW TEXT BOX
    # _________________________________________________________________________________________________________________________
    save_text_surface = font.render(save_text, True, (0, 0, 0))
    width = max(256, save_text_surface.get_width()+10)
    save_text_box.w = width
    # Blit the text.
    screen.blit(save_text_surface, (save_text_box.x+5, save_text_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, save_curr_color, save_text_box, 2)
    # _________________________________________________________________________________________________________________________

    # DRAW ALL THE BUTTONS IN BUTTON_GROUP
    button_group.update()
    button_group.draw(window)

    # SHOW DISPLAY AND UPDATE CLOCK
    pygame.display.flip()
    clock.tick(60)