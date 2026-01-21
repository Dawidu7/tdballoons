import pygame
import math

class Tower(pygame.sprite.Sprite):
  def __init__(self, x, y, targeting, effect):
    super().__init__()

    self.targeting = targeting
    self.effect = effect

    self.cooldown_timer = self.effect.cooldown

  def draw_range(self, surface, color=(0, 200, 255)):
    attack_range = getattr(self.targeting, "range", 0)
    if attack_range > 0:
      pygame.draw.circle(surface, color, self.rect.center, attack_range, 1)

  def _get_target_pos(self, target):
    if hasattr(target, "pos"):
      return pygame.Vector2(target.pos)
    if hasattr(target, "rect"):
      return pygame.Vector2(target.rect.center)
    return None

  def _rotate_towards(self, target):
    target_pos = self._get_target_pos(target)
    if not target_pos:
      return
    direction = target_pos - pygame.Vector2(self.rect.center)
    if direction.length_squared() == 0:
      return
    angle = -math.degrees(math.atan2(direction.y, direction.x))
    self.image = pygame.transform.rotate(self.base_image, angle - 270)
    self.rect = self.image.get_rect(center=self.rect.center)

  def update(self, dt, state):
    targets = self.targeting.select(self, state)
    if targets:
      target = targets[0]
      if target is not self:
        self._rotate_towards(target)

    if self.cooldown_timer > 0:
      self.cooldown_timer -= dt
      return
     
    if targets:
      self.effect.apply(self, targets, state)
      self.cooldown_timer = self.effect.cooldown