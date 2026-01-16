import pygame
from settings import *

class Game:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
      
  def update(self):
      for enemy in self.enemies:
          if enemy.hp <= 0:
              if enemy.child_type:
                  new_enemy = balloon_factory(enemy.child_type, enemy.path, self.current_difficulty)
                  new_enemy.current_point_index = enemy.current_point_index
                  new_enemy.rect.center = enemy.rect.center
                  self.enemies.add(new_enemy)
              
              self.money += enemy.reward
              enemy.kill()

    pygame.quit()

if __name__ == "__main__":
  game = Game()
  game.run()
