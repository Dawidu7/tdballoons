from abc import ABC, abstractmethod
import math
import pygame

class Tower(pygame.sprite.Sprite, ABC):
  def __init__(self, x, y, cost, damage, cooldown, attack_range):
    super().__init__()
    
    # self.image = pygame.image.load("*.png").convert_alpha()
    self.image = pygame.Surface((32, 32))
    self.image.fill((255, 0, 0))
    self.rect = self.image.get_rect(center=(x, y))

    self.cost = cost
    self.damage = damage
    self.cooldown = cooldown
    self.attack_range = attack_range

    self.last_attack_time = 0
    self.target = None

  def update(self, current_time, enemies):
    if not self._can_attack(current_time):
      return
    
    # TODO: Target validation

    if not self.target:
      self.target = self._find_target(enemies)

    if self.target:
      self.attack()
      self.last_attack_time = current_time

  def _can_attack(self, current_time):
    return current_time - self.last_attack_time >= self.cooldown

  def _find_target(self, enemies):
    closest_dist = float("inf")
    closest = None
    for enemy in enemies:
      dist = math.hypot(enemy.rect.centerx - self.rect.centerx, 
                        enemy.rect.centery - self.rect.centery)
      if dist <= self.attack_range and dist < closest_dist:
        closest_dist = dist
        closest = enemy

    return closest

  @abstractmethod
  def attack(self):
    pass
  
  @abstractmethod
  def upgrade(self):
    pass