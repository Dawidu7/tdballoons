from abc import ABC, abstractmethod
from ..projectiles import Projectile

class EffectStrategy(ABC):
  def __init__(self, damage, cooldown):
    self.damage = damage
    self.cooldown = cooldown

  @abstractmethod
  def apply(self, tower, targets, state):
    pass

class BulletEffect(EffectStrategy):
  def apply(self, tower, enemies, state):
    for enemy in enemies:
      bullet = Projectile(
        start_pos=tower.rect.center,
        target=enemy,
        damage=self.damage,
      )

      state.projectiles.add(bullet)