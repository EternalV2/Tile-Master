import pygame
from global_functions import *

class UserI(pygame.sprite.Sprite):
    def __init__(self, health, weapon_arr, minimap):
        super().__init__()
        self.heart_arr = pygame.sprite.Group()
        self.heart = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/spec/heart.png")
        self.heart = pygame.transform.scale(self.heart, (self.heart.get_width()*1.5, self.heart.get_height()*1.5))

        self.tool_bar = pygame.sprite.Group()
        
        for indx, weapon in enumerate(weapon_arr): 
            weapon.image = pygame.transform.scale(weapon.image, (weapon.image.get_width()*1.5, weapon.image.get_height()*1.5))
            half = WIDTH // 2
            weapon.rect.topleft = (half - 25 + (indx * 50), HEIGHT - 100)

            self.tool_bar.add(weapon)

        self.minimap = pygame.sprite.Group()
        minimap.image = pygame.transform.scale(minimap.image, (minimap.image.get_width()*1.7, minimap.image.get_height()*1.7))
        minimap.rect.topleft = (WIDTH - minimap.image.get_width() - 20, 20)
        self.minimap.add(minimap)

        # Create hearts according to the initial health
        self.updateHealth(health)

    def updateHealth(self, health):
        # Clear the previous hearts
        self.heart_arr.empty()

        # Create hearts according to the health
        for i in range(health):
            heart_sprite = pygame.sprite.Sprite()
            heart_sprite.image = self.heart
            heart_sprite.rect = heart_sprite.image.get_rect()
            heart_sprite.rect.topleft = (10 + (i * 50), 10)
            self.heart_arr.add(heart_sprite)

class Ui_sprite(pygame.sprite.Sprite):
    def __init__(self, name, image_name):
        
        super().__init__()
        
        self.name = name
        self.image_name = image_name
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()