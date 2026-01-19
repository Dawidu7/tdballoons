from balloons import balloon_factory

class WaveManager:
  def __init__(self, game):
    self.game = game
    self.wave = 0
    self.is_active = False
    self.queue = []
    self.spawn_timer = 0

  def start_next_wave(self):
    self.wave += 1
    self.is_active = True
    self.queue = ["red"] * (self.wave * 5)

  def update(self, dt):
    if not self.is_active:
      return
    
    if not self.queue:
      self.is_active = False
      return
    
    self.spawn_timer -= dt
    if self.spawn_timer > 0:
      return
    
    enemy_type = self.queue.pop(0)
    enemy = balloon_factory(enemy_type, self.game.map.waypoints)
    self.game.enemies.add(enemy)
    self.spawn_timer = 1
