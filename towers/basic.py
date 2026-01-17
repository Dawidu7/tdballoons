from .base import Tower

class BasicTower(Tower):
  COST = 10

  def __init__(self, x, y):
    super().__init__(x, y, damage=1, cooldown=1000, attack_range=120)
    self.image.fill((192, 192, 192))

  def attack(self):
    pass

  def upgrade(self):
    pass