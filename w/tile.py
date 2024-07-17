import pygame
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, name, walkable):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.walkable = walkable
        self.name = name
        
        self.image = pygame.image.load(self.name)
        
        self.rect = self.image.get_rect()
        self.rect.center = [self.x + (self.size // 2), self.y + (self.size // 2)] 

    # BECAUSE OF THE WAY THE LEVEL EDITOR IS SET UP, TILE.WALKABLE ISNT ACCURATE IN LEVEL_EDITOR
    # THIS IS WHY WE PASS IT INTO THE WRITE_TILE FUNCTION
    # IT MUST BE ACCURATE IN GAME_TRIAL THOUGH
    def write_tile(self, is_walkable):

        return f"|{self.x}, {self.y}, {self.size}, {self.color}, {is_walkable}, {self.name}|"

    '''
    def copy(self):
        new_version = Tile(self.x, self.y, self.size, self.color)
        new_version.image = self.image
        return new_version
    '''

    #def draw(self, screen):
        #pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
