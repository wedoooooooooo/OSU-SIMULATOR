import pygame

# this will set the visuals for the Upgrade menu.
class Menu(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y, graphic):
        super().__init__(*groups)
        self.image = pygame.image.load(graphic).convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
