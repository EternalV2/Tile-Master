import pygame
import random

from global_functions import *
from mapy import Map

f = 1

class Particle:
    def __init__(self, x, y, color_type):
        self.x = x
        self.y = y
        self.rect_x = self.x * TILE_SIZE
        self.rect_y = self.y * TILE_SIZE

        self.vel_x = random.uniform(-1, 1) / TILE_SIZE
        self.vel_y = random.uniform(-1, 1) / TILE_SIZE

        self.size = random.randint(1, 3)

        if color_type == "r":
            self.color = (255, random.randint(100, 255), 0)  # Random shade of orange
        elif color_type == "g":
            self.color = (255, 0, 0)  # Random shade of orange
        else:
            self.color = None 

        self.lifespan = random.randint(20, 40)

    def update(self, anchor, gimble):
        self.x += self.vel_x
        self.y += self.vel_y

        self.rect_x = ((self.x * TILE_SIZE) - anchor[0] - gimble[0])
        self.rect_y = ((self.y * TILE_SIZE) - anchor[1] - gimble[1])

        self.lifespan -= 1

    def draw(self, screen, camera):
        global f
        if f: 
            #print(f"DRAW PARTICLE: {self.x}, {self.y} C: {(camera.x - WIDTH) / 20}, {(camera.x + WIDTH) / 20 }")
            f= 0
        if (camera.x - WIDTH / 2 + 15) / 10 <= self.x and (camera.x + WIDTH / 2 - 15) / 10 >= self.x and (camera.y - HEIGHT / 2 + 15) / 10 <= self.y and (camera.y + HEIGHT / 2 - 15) / 10 >= self.y:
            pygame.draw.circle(screen, self.color, (int(self.rect_x), int(self.rect_y)), self.size)

class ParticleEmitter:
    def __init__(self, x, y, num_particles):
        #print(f"E, X: {x}, Y: {y}")
        self.x = x
        self.y = y
        self.rect_x = self.x * TILE_SIZE
        self.rect_y = self.y * TILE_SIZE

        self.num_particles = num_particles
        self.particles = []

    def emit_particles(self):
        #print()
        for _ in range(self.num_particles):
            particle = Particle(self.x, self.y, "r")
            self.particles.append(particle)

    def emit_particles_circular(self, collision_x, collision_y, max_radius):
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
            radius = random.uniform(0, max_radius)  # Random radius within the maximum specified radius
            x = collision_x + radius * math.cos(angle)
            y = collision_y + radius * math.sin(angle)
            particle = Particle(x, y, "g")
            self.particles.append(particle)

    def update(self, anchor, gimble):
        for particle in self.particles:
            particle.update(anchor, gimble)
            if particle.lifespan <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen, camera):
        for particle in self.particles:
            # NEED TO CHANGE BASIC BOUNDS TO WORK WITH CAMERA
            if basicBounds((particle.x, particle.y)):
                particle.draw(screen, camera)
