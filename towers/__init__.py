from .base import Tower
from .targeting import ClosestEnemy
from .effects import ProjectileEffect
from .projectiles import Projectile

class BasicTower(Tower):
  COST = 10

  def __init__(self, x, y):
    super().__init__(x, y, ClosestEnemy(100), ProjectileEffect(5, 1, Projectile))
    self.image.fill((255, 0, 0))

TOWERS = {
  "basic": BasicTower
}

def tower_factory(name, x, y):
    tower = TOWERS.get(name.lower(), BasicTower)
    return tower(x, y)