import pygame

# this is the button that will be used to open the upgrade menu.
class Button(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y, pressed_state):
        super().__init__(*groups)
        self.image = pygame.image.load(pressed_state).convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x,pos_y))