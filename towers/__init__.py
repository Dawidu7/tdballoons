from .base import Tower
from .targeting import ClosestEnemy, HighestHPEnemy
from .effects import ProjectileEffect, InstantDamageEffect
from .projectiles import Projectile

class BasicTower(Tower):
  COST = 10

  def __init__(self, x, y):
    super().__init__(x, y, ClosestEnemy(100), ProjectileEffect(5, 1, Projectile))
    self.image.fill((255, 0, 0))

class SniperTower(Tower):
  COST = 20

  def __init__(self, x, y):
    super().__init__(x, y, HighestHPEnemy(1000), InstantDamageEffect(10, 5))
    self.image.fill((192, 128, 0))

TOWERS = {
  "basic": BasicTower,
  "sniper": SniperTower
}

def tower_factory(name, x, y):
    tower = TOWERS.get(name.lower(), BasicTower)
    return tower(x, y)