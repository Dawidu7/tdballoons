import pygame

class Tower(pygame.sprite.Sprite):
  def __init__(self, x, y, targeting, effect):
    super().__init__()
    
    # self.image = pygame.image.load("*.png").convert_alpha()
    self.image = pygame.Surface((32, 32))
    self.rect = self.image.get_rect(center=(x, y))

    self.targeting = targeting
    self.effect = effect

    self.cooldown_timer = self.effect.cooldown

  def draw_range(self, surface, color=(0, 200, 255)):
    attack_range = getattr(self.targeting, "range", 0)
    if attack_range > 0:
      pygame.draw.circle(surface, color, self.rect.center, attack_range, 1)

  def update(self, dt, state):
    if self.cooldown_timer > 0:
      self.cooldown_timer -= dt
      return
     
    targets = self.targeting.select(self, state)
    if targets:
      self.effect.apply(self, targets, state)
      self.cooldown_timer = self.effect.cooldown