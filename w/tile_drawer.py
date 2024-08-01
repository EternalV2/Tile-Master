import pygame
import os
import glob
import sys

from PIL import Image
from global_functions import *
from button import Button

# TODO GETTING ERROR WHEN WE EXIT OUT OF TILE_DRAWER

# THIS IS USED SOLELY TO NAME THE OUTPUT IMAGES
# _________________________________________________________________________________________________________________________
pattern = os.path.join(IMG_DIRECTORY, "*_10.png")
tile_imgs = glob.glob(pattern)
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

# 10 X 10 PIXEL GRID WHICH IS BASIS FOR PNG IMAGE
canvas_grid = [[(255, 255, 255, 0) for _ in range(10)] for _ in range(10)]

# SETS THE DEFAULT BRUSH COLOR TO BLACK
current_color = (0, 0, 0)

# THIS IS THE VALUE GIVEN BY HOVERING OVER THE RED SLIDER
red_offset = 0

# THIS IS THE NEXT TIME YOU SHOULD CHECK WHETHER THE MOUSE IS HOVERING OVER THE RED SLIDER
poll_red_bar = 1

# THIS TOGLES WHETHER YOU SHOW THE GRID LINES (PRESS "G" TO TURN ON OR OFF)
show_gridlines = True

button_group = pygame.sprite.Group()

# BELOW SECTION HANDLES THE SET_WALKABLE BUTTON
# _________________________________________________________________________________________________________________________
# INITIALIZE THE "SET WALKABLE BUTTON" (SLIGHT TO THE LEFT OF THE CURRENT BRUSH TILE)
# WALKABLE_IMAGE SHOULD NOT BE ACCESED DIRECTLY AFTER CREATING THE BUTTON. I DONT THINK THAT WOULD MAKE SENSE
# CREATE BOTH BUTTONS AT STARTUP AND ALTERNATE THE DISPLAY BETWEEN THEM USING THE SETWALKABLE_BUTTON POINTER BASICALLY
blue_walkable_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_walkable_10_special.png"
blue_walkable_image = pygame.image.load(blue_walkable_image_name)

red_walkable_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_walkable_10_special.png"
red_walkable_image = pygame.image.load(red_walkable_image_name)

blue_walkable_button = Button(550, 360 - 25, 50, blue_walkable_image, pygame.transform.scale(blue_walkable_image, (50, 50)), blue_walkable_image_name)
red_walkable_button = Button(550, 360 - 25, 50, red_walkable_image, pygame.transform.scale(red_walkable_image, (50, 50)), red_walkable_image_name)

# DEFAULT IS_ WALKABLE = TRUE SO SET WALKABLE BUTTON WILL BE RED (TO TURN IT OFF)
set_walkable_button = red_walkable_button

# TOGGLES WHETHER THE TILE BEING CREATED IS WALKABLE
is_walkable = True
tile_transparent = False
button_group.add(set_walkable_button)
# _________________________________________________________________________________________________________________________



# _________________________________________________________________________________________________________________________
blue_t_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_t_10_special.png"
blue_t_image = pygame.image.load(blue_t_image_name)

red_t_image_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_t_10_special.png"
red_t_image = pygame.image.load(red_t_image_name)

blue_t_button = Button(700, 360 - 25, 50, blue_t_image, pygame.transform.scale(blue_t_image, (50, 50)), blue_t_image_name)
red_t_button = Button(700, 360 - 25, 50, red_t_image, pygame.transform.scale(red_t_image, (50, 50)), red_t_image_name)

# DEFAULT IS_ WALKABLE = FALSE SO SET TRANSPARENT BUTTON WILL BE BLUE (TO TURN IT ON)
set_t_button = blue_t_button

# TOGGLES WHETHER THE TILE BEING CREATED IS WALKABLE
px_transparent = False

button_group.add(set_t_button)
# _________________________________________________________________________________________________________________________


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


            # PICK COLOR (BOUNDARY CHECKS ARE FOR BLUE-GREEN GRID)
            # _________________________________________________________________________________________________________________________
            if 530 < mouse_pos[0] < 530 + 256 and 300 - 256 < mouse_pos[1] < 300: 
                #print(f"x: {mouse_pos[0]} y: {mouse_pos[1]} gr: {mouse_pos[0] - 530} bl: {mouse_pos[1] - (300 - 256)}")
                
                blue_offset = mouse_pos[0] - 530
                green_offset = mouse_pos[1] - (300 - 256)

                current_color = (red_offset, blue_offset, 256 - green_offset, 255)
            # _________________________________________________________________________________________________________________________

            # CHECK IF MOUSE IS ON CANVAS. IF IT IS, DRAW (THE 50'S HERE ARE JUST SPACE ALLOCATED FOR CANVAS DIVIDED BY NUMBER OF PIXELS)
            elif 0 < mouse_pos[0] < 500:
                if px_transparent: 
                    canvas_grid[mouse_pos[0] // 50][mouse_pos[1] // 50] = (255, 255, 255, 0)
                else:
                    canvas_grid[mouse_pos[0] // 50][mouse_pos[1] // 50] = current_color

        elif event.type == pygame.KEYDOWN:
            # TOGGLE IF THE GRID LINES ARE VISIBLE
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_g: 
                show_gridlines = not show_gridlines
            # _________________________________________________________________________________________________________________________

            # SAVE AS PNG
            # _________________________________________________________________________________________________________________________
            if event.key == pygame.K_x: 
                image = Image.new("RGBA", (10, 10))
                pixels = image.load()
                for i in range(10):
                    for j in range(10):
                        #print(f"{canvas_grid[i][j]}")
                        pixels[i, j] = canvas_grid[i][j]
                img_name = f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/output_image_{num_imgs}_10.png"
                image.save(img_name)
                num_imgs += 1
                print("Image saved as output_image.png")
                save(img_name)
            # _________________________________________________________________________________________________________________________

            # GET COLOR OF PIXEL THE MOUSE IS OVER
            # _________________________________________________________________________________________________________________________
            elif event.key == pygame.K_o: 
                mouse_pos = pygame.mouse.get_pos()
                if 0 < mouse_pos[0] < 500:
                    current_color = canvas_grid[mouse_pos[0] // 50][mouse_pos[1] // 50]
            # _________________________________________________________________________________________________________________________
    
    # Fill the window with a color (optional, for example, white)
    window.fill((255, 255, 255))

    # PRINT CANVAS
    for i in range(len(canvas_grid)):
        for j in range(len(canvas_grid[0])):
            pygame.draw.rect(window, canvas_grid[i][j], (i * (50), j * (50), 50, 50))

    # PRINT GRIDLINES
    if show_gridlines: 
        for i in range(len(canvas_grid)):
            for j in range(len(canvas_grid[0])):
                pygame.draw.rect(window, (0, 0, 0), (i * (50), j * (50), 50, 50), 2)

    # PRINT RED BAR
    for i in range(256):
            pygame.draw.rect(window, (i, 0, 0), (530 + i, 300 + 30, 1, RED_BAR_HEIGHT))
    
    # PRINT GREEN-BLUE GRID
    for i in range(256):
        for j in range(256):
            pygame.draw.rect(window, (red_offset, i, j), (530 + i, 300 - j, 1, 1))

    # PRINT THE CURRENT COLOR OF THE BRUSH ON THE RIGHT PANEL
    pygame.draw.rect(window, current_color, (625, 300 + 60, 50, 50))

    # DRAW ALL THE BUTTONS IN BUTTON_GROUP
    button_group.update()
    button_group.draw(window)

    # SHOW DISPLAY AND UPDATE CLOCK
    pygame.display.flip()
    clock.tick(60)