from .base import Tower
from .strategies.targeting import ClosestEnemy
from .strategies.effects import BulletEffect

class BasicTower(Tower):
  COST = 10

  def __init__(self, x, y):
    super().__init__(x, y, ClosestEnemy(100), BulletEffect(5, 1))
    self.image.fill((255, 0, 0))

TOWERS = {
  "basic": BasicTower
}

def tower_factory(name, x, y):
    tower = TOWERS.get(name.lower(), BasicTower)
    return tower(x, y)