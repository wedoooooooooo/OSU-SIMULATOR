import pygame

# creates a ball sprite and puts it into a single group just like above :v
class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y):
        super().__init__(*groups)

        self.image = pygame.image.load('graphics1/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x,pos_y))