from abc import ABC, abstractmethod
from assets import Assets

class EffectStrategy(ABC):
  def __init__(self, damage, cooldown):
    self.damage = damage
    self.cooldown = cooldown
    self.sound_key = None

  def play_tower_sound(self):
    if self.sound_key:
        snd = Assets.sound(self.sound_key)
        if snd:
            snd.play()

  @abstractmethod
  def apply(self, tower, targets, state):
    pass

class ProjectileEffect(EffectStrategy):
  def __init__(self, damage, cooldown, projectile, **projectile_kwargs):
    super().__init__(damage, cooldown)
    self.projectile = projectile
    self.projectile_kwargs = projectile_kwargs

  def apply(self, tower, enemies, state):
    self.play_tower_sound()
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
    self.play_tower_sound()
    for enemy in enemies:
      enemy.take_damage(self.damage)

class MoneyEffect(EffectStrategy):
  def apply(self, tower, enemies, state):
    self.play_tower_sound()
    state.money += self.damage