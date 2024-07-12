# RIPPED THIS FROM SIDEBAR.PY SO IF ANYTHING LOOKS WIERD, THATS PROBABLY WHY 
# PROBABLY SHOULD WRITE A MORE GENERAL BUTTON CLASS BUT WHATEVER

# NOTE HANDLE BUTTONS BY MAKING A 1 X 1 RECT CENTERED AT THE MOUSE POSITION AND CHECK IF THERES A COLLISION WITH A BUTTON
# LIKE THIS: mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

import pygame

from global_functions import *

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
        self.size = size

    def update_pos(self, x, y):
        self.rect.center = [x + (self.size / 2), y + (self.size)]
