import pygame
from settings import WIDTH, HEIGHT, FPS
from menu import Menu
from game import Game

class Manager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TD Balloons")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "MENU"
        self.menu = Menu(self.screen)
        self.game = None

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        selected_diff = self.menu.handle_click(event.pos)
                        if selected_diff:
                            self.game = Game(self.screen, self.clock, selected_diff)
                            self.state = "GAME"
                
                elif self.state == "GAME":
                    if self.game:
                        self.game._get_events(event)

            if self.state == "MENU":
                self.menu.draw()
            elif self.state == "GAME":
                if self.game:
                    self.game._update(dt)
                    self.game._draw()
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    manager = Manager()
    manager.run()
