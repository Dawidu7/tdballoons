import pygame

class Tower(pygame.sprite.Sprite):
  def __init__(self, x, y, targeting, effect):
    super().__init__()
    
    # self.image = pygame.image.load("*.png").convert_alpha()
    self.image = pygame.Surface((32, 32))
    self.rect = self.image.get_rect(center=(x, y))

    self.targeting = targeting
    self.effect = effect

    self.cooldown_timer = 0

  def update(self, dt, state):
    if self.cooldown_timer > 0:
      self.cooldown_timer -= dt
      return
     
    targets = self.targeting.select(self, state)
    if targets:
      self.effect.apply(self, targets, state)
      self.cooldown_timer = self.effect.cooldown