import pygame, sys
from Settings import *
from Level import Level

class Game: 
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title=TITLE)
        self.clock = pygame.time.Clock()
        self.RUN = True
        self.level = Level()
        
    def run(self):
        while self.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick(FPS_RATE) / 1000
            
            self.level.run(dt=dt)
            
            pygame.display.update()
            
if __name__ == "__main__":
    game = Game()
    game.run()