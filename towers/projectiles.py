import pygame

class Projectile(pygame.sprite.Sprite):
  def __init__(self, start_pos, target, damage, speed=400):
    super().__init__()

    self.image = pygame.Surface((10, 10))
    self.image.fill((255, 255, 0)) 
    self.rect = self.image.get_rect(center=start_pos)
    
    self.pos = pygame.Vector2(start_pos)
    self.target = target
    self.damage = damage
    self.speed = speed

  def update(self, dt):
    if not self.target.is_alive:
      self.kill()
      return

    target_pos = self.target.pos
    direction = target_pos - self.pos
    distance = direction.length()

    if distance == 0:
      self._hit()
      return

    step = self.speed * dt
    if distance <= step:
      self.pos = target_pos
      self._hit()
    else:
      self.pos += direction.normalize() * step
    
    self.rect.center = self.pos

  def _hit(self):
    if self.target.is_alive:
      self.target.take_damage(self.damage)
    self.kill()