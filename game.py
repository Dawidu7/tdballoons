import pygame
from map import Map
from sidebar import Sidebar
from balloons import balloon_factory
from towers import tower_factory, list_towers
from wave_manager import WaveManager

class Game:
  def __init__(self, screen, clock, difficulty):
    self.screen = screen
    self.clock = clock
    self.difficulty = difficulty

    self.map = Map(0.3)
    self.enemies = pygame.sprite.Group()
    self.towers = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()
    self.money = 100
    self.health = 100
    self.sidebar = Sidebar()
    self.sidebar.set_buttons(list_towers())
    self.selected_tower = None

    self.wave_manager = WaveManager(self)

  def _get_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.sidebar.handle_wave_click(event.pos, self.wave_manager.is_active):
                   self.wave_manager.start_next_wave()
                   return

                selected = self.sidebar.handle_click(event.pos)
                if selected:
                    self.selected_tower = selected
                    return
                if self.selected_tower:
                    self._try_place_tower(event.pos)

  def _update(self, dt):
        self.wave_manager.update(dt)

        self.enemies.update(dt)
        for enemy in self.enemies:
            if not enemy.is_alive:
                if hasattr(enemy, 'child_type') and enemy.child_type:
                    new_enemy = balloon_factory(enemy.child_type, self.map.waypoints, self.difficulty, 
                                                enemy.current_waypoint_index, pygame.Vector2(enemy.pos))
                    self.enemies.add(new_enemy)
                
                self.money += enemy.reward
                enemy.kill()
            
            if enemy.has_escaped:
                self.health -= enemy.damage
                enemy.kill()

        self.towers.update(dt, self)
        self.projectiles.update(dt)

  def _draw(self):
    self.screen.fill((0, 0, 0))
    self.map.draw(self.screen)
    self.enemies.draw(self.screen)
    self.towers.draw(self.screen)
    self.projectiles.draw(self.screen)
    self.sidebar.draw(self.screen, self.health, self.money, self.wave_manager.is_active, self.wave_manager.wave)

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
    if pygame.sprite.spritecollideany(tower, self.towers):
      return
    
    self.towers.add(tower)
    self.money -= tower.COST
    self.selected_tower = None