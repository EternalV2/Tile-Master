import pygame
import random

from global_functions import *

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vel, intensity):
        super().__init__()

        self.x = x
        self.y = y

        self.vel_x = vel

        # Transparent surface for the cloud
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw a rounded rectangle onto self.image
        pygame.draw.rect(
            self.image,
            (255, 255, 255, intensity),   # semi-transparent white
            self.image.get_rect(),
            border_radius=random.randint(10, 30)
        )

        # Position on screen
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    def update(self):
        self.x += self.vel_x
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)   # starting position (change as needed)
        pass
    
    def draw(self):
        pass

class Ambience:
    def __init__(self, x_range, y_range, intensity_range, width_range, height_range):
        self.clouds = []
        self.clouds_sprite = pygame.sprite.Group()

        self.x_range = x_range
        self.y_range = y_range
        self.intensity_range = intensity_range
        self.width_range = width_range
        self.height_range = height_range

    def add_clouds(self, num_clouds):
        for i in range(num_clouds):
            cloud_x = random.randint(self.x_range[0], self.x_range[1])
            cloud_y = random.randint(self.y_range[0], self.y_range[1])
            cloud_intensity = random.randint(self.intensity_range[0], self.intensity_range[1])
            cloud_vel = random.uniform(-.1, -.05)
            cloud_width = random.randint(self.width_range[0], self.width_range[1])
            cloud_height = random.randint(self.height_range[0], self.height_range[1])

            self.clouds.append(Cloud(cloud_x, cloud_y, cloud_width, cloud_height, cloud_vel, cloud_intensity))

    def update(self):
        for cloud in self.clouds:
            cloud.update()
            if cloud.x < -20:
                print(f"popped")
                cloud.x = random.randint(self.x_range[0], self.x_range[1])
                cloud_y = random.randint(self.y_range[0], self.y_range[1])

            self.clouds_sprite.add(cloud)

    def render(self):
        self.clouds_sprite.update()
        self.clouds_sprite.draw(screen)
        self.clouds_sprite.empty()