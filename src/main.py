import pygame
from settings import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.RUN = True
        
    def run(self):
        while self.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            dt = self.clock.tick() / 1000
            pygame.display.update()
            
if __name__ == "__main__":
    game = Game()
    game.run()