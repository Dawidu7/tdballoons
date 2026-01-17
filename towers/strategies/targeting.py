from abc import ABC, abstractmethod
import math

class TargetingStrategy(ABC):
  def __init__(self, range_val):
    self.range = range_val

  @abstractmethod
  def select(self, tower, state):
    pass

class ClosestEnemy(TargetingStrategy):
  def __init__(self, range_val):
    super().__init__(range_val)

  def select(self, tower, state):
    closest_dist = float("inf")
    closest = None
    for enemy in state.enemies:
      dx = enemy.rect.centerx - tower.rect.centerx
      dy = enemy.rect.centery - tower.rect.centery
      dist = math.hypot(dx, dy)
      if dist <= self.range and dist < closest_dist:
        closest_dist, closest = dist, enemy

    return [closest] if closest else []