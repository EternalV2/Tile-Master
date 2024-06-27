import pygame
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, name, walkable):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.walkable = True
        self.name = name
        
        self.image = pygame.image.load(self.name)
        
        '''
        if color == [193, 199, 40]:
            self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png")
            self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/gold_10.png"
        elif color == [58, 124, 242]:
            if random.uniform(0, 1) < .7:
                self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png")
                self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_1_10.png"
            else: 
                self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_2_10.png")
                self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/blue_2_10.png"
        else: 
            if random.uniform(0, 1) < .2:
                self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_2_10.png")
                self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_2_10.png"
            elif random.uniform(0, 1) < .2:
                self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_3_10.png")
                self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_3_10.png"
            else: 
                self.image = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png")
                self.name = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/green_1_10.png"
        '''
        self.rect = self.image.get_rect()
        self.rect.center = [self.x + (self.size // 2), self.y + (self.size // 2)] 

    def write_tile(self):
        return f"|{self.x}, {self.y}, {self.size}, {self.color}, {self.walkable}, {self.name}|"

    '''
    def copy(self):
        new_version = Tile(self.x, self.y, self.size, self.color)
        new_version.image = self.image
        return new_version
    '''

    #def draw(self, screen):
        #pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
