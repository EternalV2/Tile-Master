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
        elif color_type == "b":
            self.color = (0, 60, 90)  # Random shade of orange
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
        if (camera.x - WIDTH / 2 + 15) / TILE_SIZE <= self.x and (camera.x + WIDTH / 2 - 15) / TILE_SIZE >= self.x and (camera.y - HEIGHT / 2 + 15) / TILE_SIZE <= self.y and (camera.y + HEIGHT / 2 - 15) / TILE_SIZE >= self.y:
            pygame.draw.circle(screen, self.color, (int(self.rect_x), int(self.rect_y)), self.size)
        
    def drawOnScreen(self, screen):
        pygame.draw.circle(screen, self.color,  (int(self.x), int(self.y)), self.size)

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
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0, max_radius)
            x = collision_x + radius * math.cos(angle)
            y = collision_y + radius * math.sin(angle)
            particle = Particle(x, y, "g")
            self.particles.append(particle)

    def rain_particles(self, num_new_particles):
        for _ in range(num_new_particles):
            # HERE 100 IS JUST THE INITIAL NUMBER OF RAIN PARTICLES SO YOU DONT GET THE WEIRD INITIAL EFFECT
            if num_new_particles != 200: 
                if random.random() > .5:
                    x, y = random.randint(0, WIDTH), random.randint(0, 100)
                else:
                    x, y = random.randint(0, 100), random.randint(0, HEIGHT)
            else: 
                x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            particle = Particle(x, y, "b")
            particle.lifespan = 200
            particle.size = 4
            particle.vel_x = 16
            particle.vel_y = 16
            self.particles.append(particle)
            
    def update(self, anchor, gimble):
        for particle in self.particles:
            particle.update(anchor, gimble)
            if particle.lifespan <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen, camera):

        #num_new_particles = 0

        for particle in self.particles:
            if particle.color != (0, 60, 90):
                # NEED TO CHANGE BASIC BOUNDS TO WORK WITH CAMERA
                if basicBounds((particle.x, particle.y)):
                    particle.draw(screen, camera)

            else: 
                if particle.x > WIDTH or particle.y > HEIGHT:
                    particle.lifespan = 0
                    #num_new_particles += 1
                else:
                    particle.drawOnScreen(screen)
            
        #self.rain_particles(100-len(self.particles))
        #print(len(self.particles))