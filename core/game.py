import pygame
from balloons import balloon_factory
from core.map import Map
from core.wave_manager import WaveManager
from towers import tower_factory, list_towers
from states import GameState
from ui.sidebar import Sidebar

class Game(GameState):
  def __init__(self, manager, difficulty):
    self.manager = manager
    self.screen = manager.screen
    self.difficulty = difficulty

    self.map = Map(0.3)  # TODO: Modify straightness according to difficulty

    self.money = 100
    self.hp = 100
    self.towers = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()

    self.wave_manager = WaveManager(self)

    self.sidebar = Sidebar(self, list_towers())
    self.selected_tower = None

  def handle_event(self, event):
    match event.type:
      case pygame.MOUSEBUTTONDOWN if event.button == 1:
        if self.sidebar.handle_event(event):
          return
        
        if self.selected_tower:
          self._try_place_tower(event.pos)
      
  def update(self, dt):
      self.wave_manager.update(dt)
      if not self.wave_manager.is_active:
        return

      self.enemies.update(dt)
      self.towers.update(dt, self)
      self.projectiles.update(dt)
      
      for enemy in list(self.enemies):
        if enemy.has_escaped:
          self.hp -= enemy.damage
          enemy.kill()
          continue

        if not enemy.is_alive:
          self.money += enemy.reward

          if hasattr(enemy, 'child_type') and enemy.child_type:
            new_enemy = balloon_factory(enemy.child_type, self.map.waypoints, self.difficulty, 
                                        enemy.current_waypoint_index, pygame.Vector2(enemy.pos))
            self.enemies.add(new_enemy)
          
          enemy.kill()
          
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.map.draw(self.screen)
    self.enemies.draw(self.screen)
    self.towers.draw(self.screen)
    self.projectiles.draw(self.screen)
    self.sidebar.draw(self.screen)

    if self.selected_tower:
      pos = pygame.mouse.get_pos()
      can_place = self._can_place_tower_at(pos)
      color = (0, 255, 0) if can_place else (255, 0, 0)
      rect = pygame.Rect(0, 0, 32, 32)
      rect.center = pos

      preview = tower_factory(self.selected_tower, *pos)
      preview.draw_range(self.screen)
      pygame.draw.rect(self.screen, color, rect)

  def _can_place_tower_at(self, pos):
    x, y = pos
    if not self.map.can_place_tower(x, y):
      return False

    preview_rect = pygame.Rect(0, 0, 32, 32)
    preview_rect.center = (x, y)

    for tower in self.towers:
      if tower.rect.colliderect(preview_rect):
        return False

    return True

  def _try_place_tower(self, pos):
    if not self.map.can_place_tower(*pos):
      return
    
    tower = tower_factory(self.selected_tower, *pos)
    if self.money < tower.COST:
      return
    
    self.towers.add(tower)
    self.money -= tower.COST
    self.selected_tower = None