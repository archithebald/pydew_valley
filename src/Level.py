import pygame
from Settings import *
from Player import Player

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        
        self.setup()

    def setup(self):
        self.player = Player(group=self.all_sprites, position=(640, 360))
    
    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)