from abc import ABC, abstractmethod
import math

class TargetingStrategy(ABC):
  def __init__(self, range_val=0):
    self.range = range_val

  @abstractmethod
  def select(self, tower, state):
    pass

  def _get_enemies_in_range(self, tower, state):
    in_range = []
    range_sq = self.range ** 2

    for enemy in state.enemies:
      dx = enemy.rect.centerx - tower.rect.centerx
      dy = enemy.rect.centery - tower.rect.centery
      if dx**2 + dy**2 <= range_sq:
        in_range.append(enemy)
    
    return in_range
  
class NoTarget(TargetingStrategy):
  def select(self, tower, state):
    return [tower]

class ClosestEnemy(TargetingStrategy):
  def select(self, tower, state):
    candidates = self._get_enemies_in_range(tower, state)
    if not candidates:
      return []
    
    closest = min(candidates, key=lambda e: math.hypot(
      e.rect.centerx - tower.rect.centerx,
      e.rect.centery - tower.rect.centery
    ))
    return [closest]
  
class HighestHPEnemy(TargetingStrategy):
  def select(self, tower, state):
    candidates = self._get_enemies_in_range(tower, state)
    if not candidates:
      return []
    
    strongest = max(candidates, key=lambda e: e.hp)
    return [strongest]