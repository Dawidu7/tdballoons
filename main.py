import pygame
from core.game import Game
from ui.main_menu import MainMenu
from settings import WIDTH, HEIGHT, FPS

class Manager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TD Balloons")
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        self.go_to_menu()

    def go_to_menu(self):
        self.state = MainMenu(self)

    def go_to_difficulty(self):
        self.state = MainMenu(self)

    def go_to_game(self):
        self.state = Game(self.screen, self.clock, "Normal")

    def run(self):
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.state.handle_event(event)

            self.state.update(dt)
            
            self.state.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    manager = Manager()
    manager.run()
