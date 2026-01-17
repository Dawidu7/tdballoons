from abc import ABC, abstractmethod

class EffectStrategy(ABC):
  def __init__(self, damage, cooldown):
    self.damage = damage
    self.cooldown = cooldown

  @abstractmethod
  def apply(self, targets, state):
    pass

class DamageEffect(EffectStrategy):
  def apply(self, enemies, _):
    for enemy in enemies:
      enemy.take_damage(self.damage)