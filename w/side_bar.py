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

        # TELLS IF YOU WANT TO CYCLE THROUGH FRAME_LIST ARRAY
        self.play_state = False
        
        # TELLS IF YOU WANT TO WRITE TO EFFECTS_MAP OR BASE_MAP
        self.draw_effects = False

        self.load_tile_imgs()
    
    def load_tile_imgs(self):

        # I PURPOSELY EXCLUDED "_10_SPEC.PNG" FILES FROM HERE FOR AESTHETICS
        pattern = os.path.join(IMG_DIRECTORY, f"*_{TILE_SIZE}.png")
        tile_imgs = glob.glob(pattern)
        print(f"xxs {len(tile_imgs)}")

        # THIS IS THE FORMAT FOR THE BUTTON ARRAY (TO MAKE SURE THERE ARE 2 IMAGES IN EVERY ROWS AND ENOUGH ROWS FOR ALL THE IMAGES)
        self.button_arr = [[None for _ in range(2)] for _ in range((len(tile_imgs) // 2) + 1)]

        #print("LEN TILE IMGS: ", len(tile_imgs))

        # THIS SETS UP THE IMAGES IN THE SIDE BAR
        # _________________________________________________________________________________________________________________________
        # HERE I = J = 0 BASICALLY ACTS AS A MANUAL FOR LOOP. PROBABLY SHOULD FIX IT
        i = j = 0
        for img_name in tile_imgs:
            
            # HANDLE STATE BUTTONS (DRAW EFFECTS & PLAY STATE) GIVEN THE IMAGE NAME
            # _________________________________________________________________________________________________________________________

            # TODO TODO TODO
            # SINCE WE ARE NOT DRAWING THESE TILES BUT THEY AREE STILL ACCOUNTED FOR IN SIDEBAR SIZE, WE ARE GETTING EMPTY GAPS IN THE BAR
            # LOOKS VERY UGLY SO WORTH FIXING

            # IF THE PROGRAM IS PLAYING THE SCENES, ONLY DISPLAY THE PAUSE BUTTON
            if self.play_state:
                if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_play_10.png":
                    continue

            # IF THE PROGRAM IS PAUSED, ONLY DISPLAY THE PLAY BUTTON
            else:
                if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_pause_10.png":
                    continue
        
            '''
            if self.draw_effects:
                # IF YOU ARE DRAWING EFFECTS, SKIP DRAWING BLUE LOGO
                if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_effects_10.png":
                    continue
                
            else:
                # IF YOU ARE NOT DRAWING EFFECTS, SKIP DRAWING RED LOGO
                if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_effects_10.png":
                    continue
            '''
            # _________________________________________________________________________________________________________________________
            
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

    # RETURNS THE FRAME YOU SHOULD DRAW ON
    def handleClick(self, mouse_pos, brush, current_frame, frame_list):
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
                            
                            current_frame += 1
                            frame_list.insert(current_frame, Map(TILE_SIZE, MAP_SIZE))
                            frame_list[current_frame].load(MAP_TXT.format(current_frame - 1))

                            return current_frame

                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_left_arrow_10.png":
                            
                            return (current_frame - 1) % len(frame_list)


                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_right_arrow_10.png":
                            
                            return (current_frame + 1) % len(frame_list)
                        
                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_play_10.png":

                            self.play_state = True
                            self.load_tile_imgs()
                            return current_frame
                        
                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_pause_10.png":

                            self.play_state = False                            
                            self.load_tile_imgs()
                            return current_frame

                            '''
                            elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_effects_10.png":

                                self.draw_effects = True
                                self.load_tile_imgs()
                                return current_frame
                            '''

                        elif self.button_arr[row][col].name ==  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/red_effects_10.png":

                            self.draw_effects = True
                            brush.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/transparent_10.png")
                            brush.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/transparent_10.png"

                            #self.load_tile_imgs()
                            return current_frame

                        else:
                            brush.image = self.button_arr[row][col].real_image
                            brush.name = self.button_arr[row][col].name
                            print("IN SIDE_BAR: LABEL", self.button_arr[row][col].name)
                            print(f"hellooooooo")
                            with open(TILE_LOG_TXT, 'r') as file: 
                                for line in file:
                                    parts = line.strip().split(', ')
                                    print(f"Parts:   {parts[3]}   , Name: {self.button_arr[row][col].name}, Same: {self.button_arr[row][col].name == parts[3]}")
                                    if parts[3] == self.button_arr[row][col].name:
                                        self.draw_effects = True if parts[2] == "True" else False
                                        #print(f"bruh: {self.draw_effects}")
                                        break
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
        
        # TELLS LEVEL EDITOR TO STAY ON THE CURRENT MAP FRAME AND NOT TO CHANGE
        return current_frame