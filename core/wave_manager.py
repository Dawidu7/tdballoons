import math
import random
from balloons import BALLOON_DATA

def calculate_balloon_cost(name):
  balloon = BALLOON_DATA[name]
  cost = balloon.hp

  if balloon.child_type:
    cost += calculate_balloon_cost(balloon.child_type)

  return cost

_balloons = sorted(
  BALLOON_DATA.keys(),
  key=lambda n: calculate_balloon_cost(n)
)

BALLOONS = {}
for i, name in enumerate(_balloons):
  cost = calculate_balloon_cost(name)
  min_wave = 1 + (i * 3)
  BALLOONS[name] = {"cost": cost, "min_wave": min_wave}

class WaveManager:
  def __init__(self, game):
    self.game = game
    self.wave = 0
    self.is_active = False
    self.queue = []
    self.spawn_timer = 0
    self.current_spawn_delay  = 1.0
    self.rng = random.Random()

  def start_next_wave(self):
    if self.is_active:
      return
    
    self.wave += 1
    self.is_active = True
    self.queue = self._generate_wave_queue()
    self.spawn_timer = 0

  def update(self, dt):
    if not self.is_active:
      return
    
    if not self.queue and len(self.game.enemies) == 0 and len(self.game.projectiles) == 0:
      self.is_active = False
      return
    
    if not self.queue:
      return
    
    self.spawn_timer -= dt
    if self.spawn_timer > 0:
      return
    
    balloon_type = self.queue.pop(0)
    self.game.add_balloon(balloon_type)
    base_speed = BALLOON_DATA[balloon_type].speed
    self.spawn_timer = max(0.2, 1.0 / base_speed)

  def _generate_wave_queue(self):
    budget = math.ceil((self.wave ** self.game.diff_cfg["wave_count_mult"]) * 10)

    available = [
      (name, cfg["cost"])
      for name, cfg in BALLOONS.items()
      if cfg["min_wave"] <= self.wave
    ] or [("red", BALLOONS["red"]["cost"])]

    queue = []
    while budget > 0:
      affordable = [(n, c) for n, c in available if c <= budget]
      if not affordable:
        break

      names, costs = zip(*affordable)
      weights = [c ** 0.8 for c in costs]
      balloon_type = self.rng.choices(names, weights=weights, k=1)[0]
      balloon_cost = dict(affordable)[balloon_type]

      max_cluster = max(1, budget // balloon_cost)
      cluster_size = self.rng.randint(1, min(6, max_cluster))
      queue.extend([balloon_type] * cluster_size)
      budget -= balloon_cost * cluster_size

    return queue

