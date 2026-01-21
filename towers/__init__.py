from .base import Tower
from .targeting import *
from .effects import *
from .projectiles import *
from assets import Assets

TOWER_DATA = {
  "basic": {
    "cost": 10,
    "targeting": ClosestEnemy(100),
    "effect": ProjectileEffect(5, 1, Projectile),
    "color": (255, 0, 0),
    "asset_path": "towers.cannon1",
    "sound_path": "cannon1"
  },
  "sniper": {
    "cost": 20,
    "targeting": HighestHPEnemy(1000),
    "effect": InstantDamageEffect(10, 5),
    "color": (192, 128, 0),
    "asset_path": "towers.sniper",
    "sound_path": "sniper"
  },
  "cannon": {
    "cost": 15,
    "targeting": ClosestEnemy(100),
    "effect": ProjectileEffect(5, 1.5, AoEProjectile, radius=50),
    "color": (0, 255, 192),
    "asset_path": "towers.cannon2",
    "sound_path": "cannon2"
  },
  "farm": {
    "cost": 50,
    "targeting": NoTarget(0),
    "effect": MoneyEffect(20, 10),
    "color": (0, 255, 255),
    "asset_path": "towers.farm",
    "sound_path": "farmmoney"
  }
}

class ConfigTower(Tower):
  def __init__(self, x, y, cfg, name):
    super().__init__(x, y, cfg["targeting"], cfg["effect"])
    self.COST = cfg["cost"]
    self.name = name

    if hasattr(self.effect, 'sound_key'):
        self.effect.sound_key = cfg.get("sound_path")

    target_size = (80, 80)
    asset_name = cfg.get("asset_path")
    loaded_img = Assets.image(asset_name, size=target_size)
    if loaded_img:
        self.image = loaded_img
    else:
        self.image = pygame.Surface(target_size)
        self.image.fill(cfg["color"])
    self.rect = self.image.get_rect(center=(x, y))

def tower_factory(name, x, y):
  cfg = TOWER_DATA.get(name.lower(), TOWER_DATA["basic"])
  return ConfigTower(x, y, cfg, name)

def list_towers():
  return [(name, cfg["cost"]) for name, cfg in TOWER_DATA.items()]