import pygame

import glob
import os
from global_functions import *

class SideBar():
    def __init__(self):
        self.visible = False
        self.sidebar_sprite = pygame.sprite.Group()

        pattern = os.path.join(IMG_DIRECTORY, "*_10.png")
        tile_imgs = glob.glob(pattern)

        self.button_arr = [[None for _ in range(2)] for _ in range(len(tile_imgs) + 1)]

        i = j = 0
        for img_name in tile_imgs:

            tile_img = pygame.image.load(img_name)
            scaled_image = pygame.transform.scale(tile_img, (50, 50))
            self.button_arr[i][j] = Button(WIDTH - (75 + (j * 100)), (i * 100), 50, tile_img, scaled_image, img_name)
            self.sidebar_sprite.add(self.button_arr[i][j])

            j += 1
            if j == 2: 
                j = 0
                i += 1 
    
    def show(self, screen):
        pygame.draw.rect(screen, [117, 117, 117], (WIDTH-200, 0, 200, HEIGHT))
        
        self.sidebar_sprite.update()
        self.sidebar_sprite.draw(screen)
        
        #screen.blit(self.button_arr[row][col].image, (WIDTH - (75 + (col * 100)), (50 + (row * 100))))  # Position the image at (200, 150)

    def handleClick(self, mouse_pos, brush):
        mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        print("???????")
        for row in range(len(self.button_arr)): 
            for col in range(len(self.button_arr[0])):
                if self.button_arr[row][col] != None:
                    if mouse_rect.colliderect(self.button_arr[row][col]):
                        brush.image = self.button_arr[row][col].real_image
                        brush.name = self.button_arr[row][col].name
                        print("LABEL", self.button_arr[row][col].name)
                        break



# BASICALLY STRUCT (DATA STORAGE)
class Button(pygame.sprite.Sprite):
    # I DONT THINK THERE IS A REASON FOR SELF.X AND SELF.Y SINCE THEY ARE UNRELATED TO THE CAMERA POSITION
    def __init__(self, x, y, size, real_image, scaled_image, img_name):
        super().__init__()
        self.image = scaled_image
        self.real_image = real_image
        self.name = img_name
        self.rect = self.image.get_rect()
        self.rect.center = [x + (size / 2), y + (size)]
