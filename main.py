import pygame
from settings import *
# testowy
class TDBalloons:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TDBalloons")

    self.clock = pygame.time.Clock()

    self.running = True

  def get_events(self):
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        self.running = False

  def draw(self):
    pygame.display.flip()

  def run(self):
    while self.running:
      self.get_events()

      self.draw()

      self.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
  game = TDBalloons()
  game.run()