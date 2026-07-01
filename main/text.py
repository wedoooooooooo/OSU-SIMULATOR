import pygame

# this will define a text sprite group for all text usage.
class Text(pygame.sprite.Sprite):
    def __init__(self, *groups, font_size, text, color, pos_x, pos_y):
        super().__init__(*groups)

        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))