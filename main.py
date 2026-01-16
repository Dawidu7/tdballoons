import pygame
from settings import *
from map import Map

class Game:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    self.clock = pygame.time.Clock()

    self.running = True

    self.map = Map(0.3)
    print(self.map.waypoints)

  def get_events(self):
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        self.running = False

  def draw(self):
    self.screen.fill((0, 0, 0))

    self.map.draw(self.screen)

    pygame.display.flip()

  def run(self):
    while self.running:
      self.get_events()

      self.draw()

      self.clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
  game = Game()
  game.run()
