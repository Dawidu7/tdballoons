from abc import ABC, abstractmethod

class EffectStrategy(ABC):
  def __init__(self, damage, cooldown):
    self.damage = damage
    self.cooldown = cooldown

  @abstractmethod
  def apply(self, tower, targets, state):
    pass

class ProjectileEffect(EffectStrategy):
  def __init__(self, damage, cooldown, projectile, **projectile_kwargs):
    super().__init__(damage, cooldown)
    self.projectile = projectile
    self.projectile_kwargs = projectile_kwargs

  def apply(self, tower, enemies, state):
    for enemy in enemies:
      bullet = self.projectile(
        start_pos=tower.rect.center,
        target=enemy,
        damage=self.damage,
        state=state,
        **self.projectile_kwargs
      )

      state.projectiles.add(bullet)

class InstantDamageEffect(EffectStrategy):
  def apply(self, tower, enemies, state):
    for enemy in enemies:
      enemy.take_damage(self.damage)

class MoneyEffect(EffectStrategy):
  def apply(self, tower, enemies, state):
    if not state.wave_manager.is_active:
      return
    state.money += self.damage