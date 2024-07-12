import pygame
from global_functions import *
from particle_emitter import ParticleEmitter

class Obj(pygame.sprite.Sprite):
    def __init__(self, x, y, size, direction, animation_time, frame_time, img, anim_stack):
        super().__init__()
        
        self.x = x
        self.y = y
        self.size = size
        
        self.direction = direction

        self.next_animation = 1
        self.animation_time = animation_time

        self.next_frame = 1
        self.frame_time = frame_time

        self.degrees = getDeg(self.direction)

        if img != "": 
            self.image = pygame.transform.rotate(pygame.image.load(img), self.degrees)
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]

        else:
            self.image = None

        self.anim_stack = anim_stack

        self.emitter = ParticleEmitter(x, y, 10)

        