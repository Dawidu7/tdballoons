import pygame
from settings import *
from map import Map
from balloons import balloon_factory

class Game:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.running = True

    self.map = Map(0.3)
    self.enemies = pygame.sprite.Group()
    self.money = 0
    self.health = 100

    self.enemies.add(balloon_factory("yellow", self.map.waypoints))
    self.enemies.add(balloon_factory("yellow", self.map.waypoints))
    self.enemies.add(balloon_factory("yellow", self.map.waypoints))

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS) / 1000.0
      self.get_events()
      self.update(dt)
      self.draw()

      print(self.enemies, self.health)

  def get_events(self):
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        self.running = False

  def draw(self):
    self.screen.fill((0, 0, 0))

    self.map.draw(self.screen)
    self.enemies.draw(self.screen)

    pygame.display.flip()
      
  def update(self, dt):
    self.enemies.update(dt)
    for enemy in self.enemies:
      if enemy.has_escaped:
        self.health -= enemy.damage
        enemy.kill()

if __name__ == "__main__":
  game = Game()
  game.run()
  pygame.quit()
