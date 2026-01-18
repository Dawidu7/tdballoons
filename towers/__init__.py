from .base import Tower
from .targeting import *
from .effects import *
from .projectiles import *

TOWER_DATA = {
  "basic": {
    "cost": 10,
    "targeting": ClosestEnemy(100),
    "effect": ProjectileEffect(5, 1, Projectile),
    "color": (255, 0, 0),
  },
  "sniper": {
    "cost": 20,
    "targeting": HighestHPEnemy(1000),
    "effect": InstantDamageEffect(10, 5),
    "color": (192, 128, 0),
  },
  "cannon": {
    "cost": 15,
    "targeting": ClosestEnemy(100),
    "effect": ProjectileEffect(5, 1.5, AoEProjectile, radius=50),
    "color": (0, 255, 192)
  },
  "farm": {
    "cost": 50,
    "targeting": NoTarget(0),
    "effect": MoneyEffect(20, 10),
    "color": (0, 255, 255)
  }
}

class ConfigTower(Tower):
  def __init__(self, x, y, cfg):
    super().__init__(x, y, cfg["targeting"], cfg["effect"])
    self.COST = cfg["cost"]
    self.image.fill(cfg["color"])

def tower_factory(name, x, y):
  cfg = TOWER_DATA.get(name.lower(), TOWER_DATA["basic"])
  return ConfigTower(x, y, cfg)

def list_towers():
  return [(name, cfg["cost"]) for name, cfg in TOWER_DATA.items()]