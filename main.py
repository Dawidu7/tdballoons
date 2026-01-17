import pygame
from settings import *
from map import Map
from balloons import balloon_factory
from towers import tower_factory

class Game:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.running = True

    self.map = Map(0.3)
    self.enemies = pygame.sprite.Group()
    self.towers = pygame.sprite.Group()
    self.money = 100
    self.health = 100

    # self.enemies.add(balloon_factory("yellow", self.map.waypoints))

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS) / 1000.0
      self._get_events()
      self._update(dt)
      self._draw()
      print(self.money)

  def _get_events(self):
    for e in pygame.event.get():
      match e.type:
        case pygame.QUIT:
          self.running = False
        case pygame.MOUSEBUTTONDOWN:
          if e.button == 1:
            self._try_place_tower(e.pos)

  def _update(self, dt):
    self.enemies.update(dt)
    for enemy in self.enemies:
      if enemy.has_escaped:
        self.health -= enemy.damage
        enemy.kill()

  def _draw(self):
    self.screen.fill((0, 0, 0))

    self.map.draw(self.screen)
    self.enemies.draw(self.screen)
    self.towers.draw(self.screen)

    pygame.display.flip()

  def _try_place_tower(self, pos):
    if not self.map.can_place_tower(*pos):
      return
    
    tower = tower_factory("basic", *pos)

    if self.money < tower.COST:
      return
    if pygame.sprite.spritecollideany(tower, self.towers):
      return
    
    self.towers.add(tower)
    self.money -= tower.COST

if __name__ == "__main__":
  game = Game()
  game.run()
  pygame.quit()
