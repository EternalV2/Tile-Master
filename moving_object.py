import pygame
import random

from global_functions import *
from mapy import Map
from particle_emitter import Particle, ParticleEmitter

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, direction, team):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.direction = direction

        self.delete_time = 1

        self.team = team

        self.image = pygame.image.load("img/fireball/fireball_u.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

        self.animStack = []

        self.next_animation = 1
        self.animation_time = 35*3

        self.next_frame = 1
        self.frame_time = 25

        self.degrees = getDeg(self.direction)
        self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_u.png"), self.degrees)
        
        self.animStack.append("img/fireball/fireball_spawn4.png")
        self.animStack.append("img/fireball/fireball_spawn3.png")
        self.animStack.append("img/fireball/fireball_spawn2.png")
        self.animStack.append("img/fireball/fireball_spawn1.png")

        self.count = random.randint(0, 7)

        self.emitter = ParticleEmitter(x, y, 10)

    def move(self):
        # Update the position only when the move counter reaches the move frequency        
        if self.animStack:
            time_now = pygame.time.get_ticks()
            
            if time_now < self.next_animation: 
                return

            self.next_animation = time_now + self.animation_time
            
            self.image = pygame.image.load(self.animStack.pop())
            self.image = pygame.transform.rotate(self.image, self.degrees)
            return 

        if self.direction == 'lu':
            self.x -= TILE_SIZE
            self.y -= TILE_SIZE
        elif self.direction == 'ld':
            self.x -= TILE_SIZE
            self.y += TILE_SIZE
        elif self.direction == 'ru':
            self.x += TILE_SIZE
            self.y -= TILE_SIZE
        elif self.direction == 'rd':
            self.x += TILE_SIZE
            self.y += TILE_SIZE
        elif self.direction == 'r':
            self.x += TILE_SIZE
        elif self.direction == 'l':
            self.x -= TILE_SIZE
        elif self.direction == 'd':
            self.y += TILE_SIZE
        elif self.direction == 'u':
            self.y -= TILE_SIZE

        self.emitter.x = self.x
        self.emitter.y = self.y
        self.emitter.emit_particles()

        time_delta = checkTime(self.next_frame, self.frame_time)
        if time_delta ==-1:
            return
        else:
            self.next_frame = time_delta

        if self.count == 0:
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u0.png"), self.degrees)
            self.count = 1
        elif self.count == 1: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u1.png"), self.degrees)
            self.count = 2
        elif self.count == 2: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u2.png"), self.degrees)
            self.count = 3
        elif self.count == 3: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u3.png"), self.degrees)
            self.count = 4
        elif self.count == 4: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u4.png"), self.degrees)
            self.count = 5
        elif self.count == 5: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u5.png"), self.degrees)
            self.count = 6
        elif self.count == 6: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u6.png"), self.degrees)
            self.count = 7
        elif self.count == 7: 
            self.image = pygame.transform.rotate(pygame.image.load("img/fireball/fireball_movement_2.0/fireball_u7.png"), self.degrees)
            self.count = 0

        self.rect.center = [self.x, self.y]

        # THIS IS FOR SELF DELETION
        if not inMap(self.x, self.y, self.direction, self.size):
            if self.delete_time == 1:
                self.delete_time = time_now = pygame.time.get_ticks() + 1500
            return -1

        else:
            return 1
