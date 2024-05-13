import pygame

class UserI(pygame.sprite.Sprite):
    def __init__(self, health):
        super().__init__()
        self.heart_arr = pygame.sprite.Group()
        self.heart = pygame.image.load("/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/heart.png")
        self.heart = pygame.transform.scale(self.heart, (self.heart.get_width()*1.5, self.heart.get_height()*1.5))

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
