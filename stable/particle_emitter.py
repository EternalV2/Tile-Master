import pygame
import random

from global_functions import *
from mapy import Map

class Particle:
    def __init__(self, x, y, color_type):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 1)
        self.size = random.randint(1, 3)

        if color_type == "r":
            self.color = (255, random.randint(100, 255), 0)  # Random shade of orange
        elif color_type == "g":
            self.color = (255, 0, 0)  # Random shade of orange
        else:
            self.color = None 

        self.lifespan = random.randint(20, 40)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ParticleEmitter:
    def __init__(self, x, y, num_particles):
        self.x = x
        self.y = y
        self.num_particles = num_particles
        self.particles = []

    def emit_particles(self):
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

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            if basicBounds(particle.x, particle.y):
                particle.draw(screen)
