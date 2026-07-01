import pygame

## creates a player sprite containing the image (1), fill (2) and default position (3).
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y):
        super().__init__(*groups)

        self.image = pygame.image.load('assets/graphics1/blue.png').convert_alpha() # (1)
        self.image.fill('blue') # (2)
        self.rect = self.image.get_rect(center = (pos_x,pos_y)) # (3)