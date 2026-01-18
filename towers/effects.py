from abc import ABC, abstractmethod

class EffectStrategy(ABC):
  def __init__(self, damage, cooldown):
    self.damage = damage
    self.cooldown = cooldown

  @abstractmethod
  def apply(self, tower, targets, state):
    pass

class ProjectileEffect(EffectStrategy):
  def __init__(self, damage, cooldown, projectile):
    super().__init__(damage, cooldown)
    self.projectile = projectile

  def apply(self, tower, enemies, state):
    for enemy in enemies:
      bullet = self.projectile(
        start_pos=tower.rect.center,
        target=enemy,
        damage=self.damage,
      )

      state.projectiles.add(bullet)

class InstantDamageEffect(EffectStrategy):
  def apply(self, tower, enemies, state):
    for enemy in enemies:
      enemy.take_damage(self.damage)