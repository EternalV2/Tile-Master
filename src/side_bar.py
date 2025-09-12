import pygame

import glob
import os
import sys
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

        self.text_group = pygame.sprite.Group()

        self.load_tile_imgs(f"*_{TILE_SIZE}.png")
    
    def load_tile_imgs(self, extension):

        # TODO THIS IS INEFFICENT CODE (CHECKING EXTENSION != .MP3 TWICE) MAKE IT NICER.
        if str(extension) != "*.mp3": 
            pattern = os.path.join(f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/stable/{MAP_NAME}/_{TILE_SIZE}", extension)
        else:
            pattern = os.path.join(f"/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/", extension)

        # I PURPOSELY EXCLUDED "_10_SPEC.PNG" FILES FROM HERE FOR AESTHETICS
        print(f"P: {pattern}")
        tile_imgs = glob.glob(pattern)
        print(f"tile: {tile_imgs}")
        print(f"xxs {len(tile_imgs)}")

        # THIS IS THE FORMAT FOR THE BUTTON ARRAY (TO MAKE SURE THERE ARE 2 IMAGES IN EVERY ROWS AND ENOUGH ROWS FOR ALL THE IMAGES)
        self.button_arr = [[None for _ in range(2)] for _ in range((len(tile_imgs) // 2) + 1)]

        #print("LEN TILE IMGS: ", len(tile_imgs))

        # THIS SETS UP THE IMAGES IN THE SIDE BAR
        # _________________________________________________________________________________________________________________________
        # HERE I = J = 0 BASICALLY ACTS AS A MANUAL FOR LOOP. PROBABLY SHOULD FIX IT
        
        tiles_in_log = set()
        
        with open(TILE_LOG_TXT, 'r') as file: 
            for line in file:
                parts = line.strip().split(', ')
                print(f"parts: {parts}")
                tiles_in_log.add(parts[3])
        
        print("asd", extension)
        i = j = 0

        for img_name in tile_imgs:
            print(f"img_name: {img_name}, tiles in log: {tiles_in_log}")
            
            if str(extension) != "*.mp3" and img_name not in tiles_in_log:
                continue
            else:
                print(f"hit: {img_name}")
            
            print(f"done")
            wonder = str(extension) == "*.mp3"
            print(f"wnder {wonder}")
            print(f"pattern {extension}")
            if extension != "*.mp3":
                # HANDLE STATE BUTTONS (DRAW EFFECTS & PLAY STATE) GIVEN THE IMAGE NAME
                # _________________________________________________________________________________________________________________________

                # TODO TODO TODO
                # SINCE WE ARE NOT DRAWING THESE TILES BUT THEY AREE STILL ACCOUNTED FOR IN SIDEBAR SIZE, WE ARE GETTING EMPTY GAPS IN THE BAR
                # LOOKS VERY UGLY SO WORTH FIXING

                # IF THE PROGRAM IS PLAYING THE SCENES, ONLY DISPLAY THE PAUSE BUTTON
                if self.play_state:
                    if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_play_10.png":
                        continue

                # IF THE PROGRAM IS PAUSED, ONLY DISPLAY THE PLAY BUTTON
                else:
                    if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_pause_10.png":
                        continue
                '''
                if self.draw_effects:
                    # IF YOU ARE DRAWING EFFECTS, SKIP DRAWING BLUE LOGO
                    if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/blue_effects_10.png":
                        continue
                    
                else:
                    # IF YOU ARE NOT DRAWING EFFECTS, SKIP DRAWING RED LOGO
                    if img_name == "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_effects_10.png":
                        continue
                '''
                # _________________________________________________________________________________________________________________________

                tile_img = pygame.image.load(img_name)
                print(f"Loaded")
            
            else: 
                print(f"swithed")
                tile_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/music_10.png")
                print(f"\nMUSIC: img_name: {img_name.strip().split('/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/')}")

                # INITIALIZE THE FONTS
                # _________________________________________________________________________________________________________________________
                font = pygame.font.Font(None, 15)

                # Create a text sprite and add it to the group
                #text_sprite = TextSprite(str(img_name.strip().split('/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/')[1]), font, (255, 255, 255), (100, 100))
                text_str = str(img_name.strip().split('/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/')[1])
                
                new_text = []
                word = []
                for char in text_str:
                    if len(word) > 12:
                        new_text.append("".join(word))
                        word = []
                    word.append(char)
                
                if word != []:
                    new_text.append("".join(word))

                print(f"NEW TEXT: {new_text}, TEXT STRING: {text_str}")
                for line_number, line in enumerate(new_text):
                    print(line, line_number)
                    text_sprite = TextSprite(line, font, (255, 255, 255), (WIDTH - (175 - (j * 100) - 25), (i * 100) + 85 + (line_number * 15)))
                    self.text_group.add(text_sprite)
                # _________________________________________________________________________________________________________________________

            # RESCALE BEAUSE 10 X 10 PIXELS ISN'T ENOUGH FOR THE SIDEBAR

            scaled_image = pygame.transform.scale(tile_img, (50, 50))
            
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

                        brush.image = self.button_arr[row][col].real_image
                        brush.name = self.button_arr[row][col].name


                        print("IN SIDE_BAR: LABEL", self.button_arr[row][col].name)
                        print(f"hellooooooo")
                        with open(TILE_LOG_TXT, 'r') as file: 
                            for line in file:
                                parts = line.strip().split(', ')
                                if parts[3] == self.button_arr[row][col].name:
                                    print(f"parts:{parts}")
                                    print(f"Parts:   {parts[3]}   , Name: {self.button_arr[row][col].name}, Same: {self.button_arr[row][col].name == parts[3]}")
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
class LeftBar():
    def __init__(self):
        self.visible = False
        self.leftbar_sprite = pygame.sprite.Group()

        self.button_arr = []
        
        self.play_state = False

        # BRUSH HAS ITS OWN FILL BOOL BUT THIS IS FOR UI
        self.fill_bucket = False
        self.show_music = False

        self.num_imgs = 8

        self.load_tile_imgs()

    def load_tile_imgs(self):
        self.leftbar_sprite = pygame.sprite.Group()

        # I PURPOSELY EXCLUDED "_10_SPEC.PNG" FILES FROM HERE FOR AESTHETICS
        
        # INDEXES FOR SPECIFIC BUTTONS:
        # WHITE PLUS - 0
        # RED PLUS - 1
        # RED PLAY/PAUSE - 2
        # RED RIGHT - 3
        # RED LEFT - 4
        # RED EFFECTS - 5
        # RED/BLUE BUCKETS - 6
        # MUSIC - 7

        white_plus_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/white_plus_10.png")
        white_plus_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/white_plus_10.png"
        white_plus_scaled = pygame.transform.scale(white_plus_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (0 * 75), 50, white_plus_img, white_plus_scaled, white_plus_name))
        self.leftbar_sprite.add(self.button_arr[-1])

        red_plus_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_plus_10.png")
        red_plus_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_plus_10.png"
        red_plus_scaled = pygame.transform.scale(red_plus_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (1 * 75), 50, red_plus_img, red_plus_scaled, red_plus_name))
        self.leftbar_sprite.add(self.button_arr[-1])
                                                  
        if not self.play_state:
            red_play_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_play_10.png")
            red_play_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_play_10.png"
            red_play_scaled = pygame.transform.scale(red_play_img, (50, 50))
            self.button_arr.append(Button(25, 100 + (2 * 75), 50, red_play_img, red_play_scaled, red_play_name))
            self.leftbar_sprite.add(self.button_arr[-1])

        else: 
            red_pause_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_pause_10.png")
            red_pause_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_pause_10.png"
            red_pause_scaled = pygame.transform.scale(red_pause_img, (50, 50))
            self.button_arr.append(Button(25, 100 + (2 * 75), 50, red_pause_img, red_pause_scaled, red_pause_name))
            self.leftbar_sprite.add(self.button_arr[-1])

        red_right_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_right_arrow_10.png")
        red_right_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_right_arrow_10.png"
        red_right_scaled = pygame.transform.scale(red_right_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (3 * 75), 50, red_right_img, red_right_scaled, red_right_name))
        self.leftbar_sprite.add(self.button_arr[-1])

        red_left_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_left_arrow_10.png")
        red_left_name =  "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_left_arrow_10.png"
        red_left_scaled = pygame.transform.scale(red_left_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (4 * 75), 50, red_left_img, red_left_scaled, red_left_name))
        self.leftbar_sprite.add(self.button_arr[-1])
        
        red_effects_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_effects_10.png")
        red_effects_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_effects_10.png"
        red_effects_scaled = pygame.transform.scale(red_effects_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (5 *75), 50, red_effects_img, red_effects_scaled, red_effects_name))
        self.leftbar_sprite.add(self.button_arr[-1])

        if not self.fill_bucket:
            red_play_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/blue_bucket_10.png")
            red_play_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/blue_bucket_10.png"
            red_play_scaled = pygame.transform.scale(red_play_img, (50, 50))
            self.button_arr.append(Button(25, 100 + (6 * 75), 50, red_play_img, red_play_scaled, red_play_name))
            self.leftbar_sprite.add(self.button_arr[-1])

        else: 
            red_pause_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_bucket_10.png")
            red_pause_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/red_bucket_10.png"
            red_pause_scaled = pygame.transform.scale(red_pause_img, (50, 50))
            self.button_arr.append(Button(25, 100 + (6 * 75), 50, red_pause_img, red_pause_scaled, red_pause_name))
            self.leftbar_sprite.add(self.button_arr[-1])

        music_img = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/music_10.png")
        music_name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/music_10.png"
        music_scaled = pygame.transform.scale(music_img, (50, 50))
        self.button_arr.append(Button(25, 100 + (7 * 75), 50, music_img, music_scaled, music_name))
        self.leftbar_sprite.add(self.button_arr[-1])

        print(f"Len: {len(self.button_arr)}")

    # RETURNS THE FRAME YOU SHOULD DRAW ON
    def handleClick(self, mouse_pos, brush, current_frame, frame_list, sidebar):
        # MAKE A RECTANGLE CENTERED AT THE MOUSE POSITION TO USE INBUILT COLLISION DETETION TO SEE IF A BUTTON IS CLICKED
        mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        print(f"mouse_pos: {mouse_pos}")
        print(f"self.button_arr: {self.button_arr[0]}")
        if mouse_rect.colliderect(self.button_arr[0]):
            # RUN TILE_DRAWER. WHILE IT RUNS, CAN'T USE LEVEL_EDITOR
            print("running tile_drawer")
            os.system(f'"{sys.executable}" tile_drawer.py')

        elif mouse_rect.colliderect(self.button_arr[1]):
            save()
            current_frame += 1
            frame_list.insert(current_frame, Map(TILE_SIZE, MAP_SIZE))
            frame_list[current_frame].load(MAP_TXT.format(current_frame - 1))
            save()
            return current_frame
        
        elif mouse_rect.colliderect(self.button_arr[2]):
            self.play_state = not self.play_state
            #self.load_tile_imgs(f"*_{TILE_SIZE}.png")
            self.load_tile_imgs()
            return current_frame

        elif mouse_rect.colliderect(self.button_arr[3]):
            
            print(f"Front: {(current_frame + 1) % len(frame_list)}" )
            return (current_frame + 1) % len(frame_list)

        elif mouse_rect.colliderect(self.button_arr[4]):
            print(f"Back: {(current_frame - 1) % len(frame_list)}" )
            return (current_frame - 1) % len(frame_list)
        
        elif mouse_rect.colliderect(self.button_arr[5]):
            
            brush.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/transparent_10.png")
            brush.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/transparent_10.png"
            
            sidebar.draw_effects = True
            print("draw effects")
            return current_frame
        
        elif mouse_rect.colliderect(self.button_arr[6]):
            self.fill_bucket = not self.fill_bucket
            brush.fill = self.fill_bucket

            self.load_tile_imgs()
            print(f"bucket")
            return current_frame

        elif mouse_rect.colliderect(self.button_arr[7]):
            self.show_music = not self.show_music
            print(f"Clicked Music")
            if self.show_music:
                print("MP3 MODE")
            else:
                print("IMG MODE")

            return current_frame

        # TELLS LEVEL EDITOR TO STAY ON THE CURRENT MAP FRAME AND NOT TO CHANGE
        return current_frame
    
    def show(self, screen):

        # THIS USED TO BE IN LOAD_TILE_IMGS BUT I MOVED IT TO IMPLEMENT SELF.SCROLL_OFFSET
        # THIS AGAIN SHOWS HOW IMPORTANT IT IS TO SEPERATE SCREEN POSITION (WHERE THE OBJECT RENDERS) FROM BACKEND (POSITION IN THE ACTUAL DATA STRUCUTRES)
        # _________________________________________________________________________________________________________________________
        pygame.draw.rect(screen, [117, 117, 117], (0, 100, 100, (self.num_imgs * 75) + 25))

        #print(f"big big: {len(self.button_arr)}")
        # _________________________________________________________________________________________________________________________

        self.leftbar_sprite.update()
        self.leftbar_sprite.draw(screen)
        
        #screen.blit(self.button_arr[row][col].image, (WIDTH - (75 + (col * 100)), (50 + (row * 100))))  # Position the image at (200, 150)

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, position):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=position)
