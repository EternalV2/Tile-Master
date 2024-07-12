import pygame

import glob
import os
from global_functions import *
from button import Button

class SideBar():
    def __init__(self):
        # TOGLE IF THE SIDEBAR IS VISIBLE (PRESS "+" TO TOGLE)
        self.visible = False
        self.sidebar_sprite = pygame.sprite.Group()

        self.button_arr = []

        # THIS IS FOR SCROLLING THROUGH THE SIDEBAR
        self.scroll_offset = 0

        self.load_tile_imgs()
    
    def load_tile_imgs(self):

        # I PURPOSELY EXCLUDED "_10_SPEC.PNG" FILES FROM HERE FOR AESTHETICS
        pattern = os.path.join(IMG_DIRECTORY, "*_10.png")
        tile_imgs = glob.glob(pattern)

        # THIS IS THE FORMAT FOR THE BUTTON ARRAY (TO MAKE SURE THERE ARE 2 IMAGES IN EVERY ROWS AND ENOUGH ROWS FOR ALL THE IMAGES)
        self.button_arr = [[None for _ in range(2)] for _ in range((len(tile_imgs) // 2) + 1)]

        #print("LEN TILE IMGS: ", len(tile_imgs))

        # THIS SETS UP THE IMAGES IN THE SIDE BAR
        # _________________________________________________________________________________________________________________________
        # HERE I = J = 0 BASICALLY ACTS AS A MANUAL FOR LOOP. PROBABLY SHOULD FIX IT
        i = j = 0
        for img_name in tile_imgs:
            tile_img = pygame.image.load(img_name)
            # RESCALE BEAUSE 10 X 10 PIXELS ISN'T ENOUGH FOR THE SIDEBAR
            scaled_image = pygame.transform.scale(tile_img, (50, 50))
            
            # DEPRECATED FUCK THIS SHIT
            '''
            # THIS IF STATEMENT MAKES SURE THE WHITE PLUS IS RENDEDRED AS THE LAST BOX IN THE BUTTON ARRAY
            if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/white_plus_10.png":

                ###
                # WAY TO DIRTY: WAS len(tile_imgs) % 2 IN 3 PLACES. CHANGED IT TO (len(tile_imgs) + 1) % 2

                #self.button_arr[len(self.button_arr) - 2][(len(tile_imgs) + 1) % 2] = Button(WIDTH - (75 + (((len(tile_imgs) + 1) % 2) * 100)), ((len(self.button_arr) - 2) * 100), 50, tile_img, scaled_image, img_name)    
                #self.sidebar_sprite.add(self.button_arr[len(self.button_arr) - 2][(len(tile_imgs) + 1) % 2])
                ###

                self.button_arr[len(self.button_arr) - 1][(len(tile_imgs) + 1) % 2] = Button(WIDTH - (175 - (((len(tile_imgs) + 1) % 2) * 100)), ((len(self.button_arr)) * 100), 50, tile_img, scaled_image, img_name)    
                self.sidebar_sprite.add(self.button_arr[len(self.button_arr) - 1][(len(tile_imgs) + 1) % 2])
                
                print(f"last row {((len(tile_imgs) + 1) % 2)}, pos row: {WIDTH - (175 - (((len(tile_imgs) + 1) % 2) * 100))}, last col: {(len(self.button_arr) - 1)}, pos col {((len(self.button_arr)) * 100)}")
            else:
            '''

            #print(f"i {i}, y: {i * 100}, j {j}, x: {WIDTH - (75 + (j * 100))}")

            self.button_arr[i][j] = Button(WIDTH - (175 - (j * 100)), (i * 100), 50, tile_img, scaled_image, img_name)

            # MANUAL FOR LOOP UPDATES. PROBABLY SHOULD REDO
            # _________________________________________________________________________________________________________________________
            j += 1
            if j == 2: 
                j = 0
                i += 1
            # _________________________________________________________________________________________________________________________
        # _________________________________________________________________________________________________________________________

    def show(self, screen):

        # THIS USED TO BE IN LOAD_TILE_IMGS BUT I MOVED IT TO IMPLEMENT SELF.SCROLL_OFFSET
        # THIS AGAIN SHOWS HOW IMPORTANT IT IS TO SEPERATE SCREEN POSITION (WHERE THE OBJECT RENDERS) FROM BACKEND (POSITION IN THE ACTUAL DATA STRUCUTRES)
        # _________________________________________________________________________________________________________________________
        self.sidebar_sprite = pygame.sprite.Group()
        pygame.draw.rect(screen, [117, 117, 117], (WIDTH-200, 0, 200, HEIGHT))

        for i in range(len(self.button_arr)):
            for j in range (len(self.button_arr[i])):
                if self.button_arr[i][j] != None:
                    
                    # DIFFERENCE BETWEEN THIS LINE AND THE LINE IN LOAD_TILE_POSITIONS IS WE HANDLE THE SCROLL OFFSET
                    self.button_arr[i][j].update_pos(WIDTH - (175 - (j * 100)), ((i - self.scroll_offset) * 100))
                    
                    self.sidebar_sprite.add(self.button_arr[i][j])
        # _________________________________________________________________________________________________________________________

        self.sidebar_sprite.update()
        self.sidebar_sprite.draw(screen)
        
        #screen.blit(self.button_arr[row][col].image, (WIDTH - (75 + (col * 100)), (50 + (row * 100))))  # Position the image at (200, 150)

    def handleClick(self, mouse_pos, brush, full_map):
        # MAKE A RECTANGLE CENTERED AT THE MOUSE POSITION TO USE INBUILT COLLISION DETETION TO SEE IF A BUTTON IS CLICKED
        mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        
        # ITERATE THROUGH ALL BUTTONS TO SEE WHICH (IF ANY) IS CLICKED. ONCE YOU FIND THE BUTTON, BREAK OUT
        for row in range(len(self.button_arr)): 
            for col in range(len(self.button_arr[0])):
                
                # THIS SHOULD ONLY BE NONE IF ITS THE LAST ROW AND THERE IS ONLY 1 IMAGE INSIDE IT. THEN THE 2ND SLOT WILL BE DEFAULT SET TO NONE.
                # NOT TESTED EXTENSIVELY
                if self.button_arr[row][col] != None:
                    if mouse_rect.colliderect(self.button_arr[row][col]):
                        if self.button_arr[row][col].name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/white_plus_10.png":
                            # RUN TILE_DRAWER. WHILE IT RUNS, CAN'T USE LEVEL_EDITOR
                            os.system("python3 tile_drawer.py")
                            self.load_tile_imgs()
                            print("IN SIDE BAR: WE OUT")
                        
                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_plus_10.png":
                            
                            full_map.anim_stack.append([])
                            return

                        else:
                            brush.image = self.button_arr[row][col].real_image
                            brush.name = self.button_arr[row][col].name
                            print("IN SIDE_BAR: LABEL", self.button_arr[row][col].name)

                            # NOTE
                            # _________________________________________________________________________________________________________________________
                            # THIS CODE DOES NOT HANDLE IS_WALKABLE. ACCORDING TO THE BRUSH, ITS ALL THE SAME
                            # IS_WALKABLE IS HANDLED IN THE SAVE METHOD OF LEVEL_EDITOR
                            # IT DELVES INTO THE TILE_LOG_TXT FILE AND MATCHES THE NAME WITH THE IS_WALKABLE ATTRIBUTE FOR THE TILE
                            # THE BRUSH DOES NOT HANDLE IS_WALKABLE LIKE IT DOES WITH IMAGE AND NAME
                            # TO FIND THE CONTROL FLOW GO LEVEL_EDITOR -> SAVE -> TILE.WRITE_TILE
                            # HOPEFULLY THESE COMMENTS KEEP ME FROM MESSING UP THIS SPAGHETTI ASS LOOKING CODE
                            # _________________________________________________________________________________________________________________________

                            # THE BREAK IS FOR EFFICENCY (NO NEED TO CHECK REST OF BUTTONS IF YOU ALREADY FOUND THE CLICKED ONE)
                            break