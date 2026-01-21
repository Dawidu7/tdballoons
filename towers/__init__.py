from dataclasses import dataclass
from typing import Callable
from assets import Assets
from .base import Tower
from .effects import *
from .projectiles import *
from .targeting import *

@dataclass(frozen=True)
class TowerConfig:
  name: str
  cost: int
  targeting: Callable[[], TargetingStrategy]
  effect: Callable[[], EffectStrategy]
  image_path: str
  sound_path: str

TOWERS = {
  "basic": TowerConfig(
    name="basic",
    cost=10,
    targeting=lambda: ClosestEnemy(100),
    effect=lambda: ProjectileEffect(5, 1, Projectile),
    image_path="cannon1",
    sound_path="cannon1"
  ),
  "sniper": TowerConfig(
    name="sniper",
    cost=20,
    targeting=lambda: HighestHPEnemy(1000),
    effect=lambda: InstantDamageEffect(10, 5),
    image_path="sniper",
    sound_path="sniper"
  ),
  "cannon": TowerConfig(
    name="cannon",
    cost=15,
    targeting=lambda: ClosestEnemy(100),
    effect=lambda: ProjectileEffect(5, 1.5, AoEProjectile, radius=50),
    image_path="cannon2",
    sound_path="cannon2"
  ),
  "farm": TowerConfig(
    name="farm",
    cost=50,
    targeting=lambda: NoTarget(0),
    effect=lambda: MoneyEffect(20, 10),
    image_path="farm",
    sound_path="farmmoney"
  ),
}

def tower_factory(name, x, y):
  cfg = TOWERS.get(name.lower(), TOWERS["basic"])

  targeting = cfg.targeting()
  effect = cfg.effect()

  tower = Tower(targeting, effect)
  tower.cost = cfg.cost
  tower.name = cfg.name

  if hasattr(tower.effect, "sound_key"):
    tower.effect.sound_key = cfg.sound_path

  size = (80, 80)
  loaded_img = Assets.image(f"towers.{cfg.image_path}", size=size)
  if loaded_img:
    tower.base_image = loaded_img
  else:
    tower.base_image = pygame.Surface(size)
    tower.base_image.fill((192, 0, 0))

  tower.image = tower.base_image.copy()
  tower.rect = tower.image.get_rect(center=(x, y))

  return tower

def list_towers():
  return [(name, cfg.cost) for name, cfg in TOWERS.items()]