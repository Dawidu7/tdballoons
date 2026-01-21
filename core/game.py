import pygame
from balloons import balloon_factory
from towers import tower_factory, list_towers
from states import GameState
from ui.sidebar import Sidebar
from assets import Assets
from .map import Map
from .save_manager import SaveManager
from .wave_manager import WaveManager

class Game(GameState):
  def __init__(self, manager, difficulty=None, save_data=None):
    self.manager = manager
    self.screen = manager.screen
    
    if save_data:
      self.difficulty = save_data["difficulty"]
      self.money = save_data["money"]
      self.hp = save_data["hp"]
      map_seed = save_data["map_seed"]
      straightness = save_data["map_straightness"]
      start_wave = save_data["wave"]
    else:
      self.difficulty = difficulty or "normal"
      self.money = 100
      self.hp = 100
      map_seed = None
      straightness = 0.3
      start_wave = 0

    self.map = Map(straightness, map_seed)

    self.towers = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()

    if save_data:
      for t in save_data["towers"]:
        tower = tower_factory(t["type"], t["x"], t["y"])
        self.towers.add(tower)

    self.wave_manager = WaveManager(self)
    self.wave_manager.wave = start_wave
    self.was_wave_active = False

    self.sidebar = Sidebar(self, list_towers())
    self.selected_tower = None

    self.save_font = pygame.font.SysFont("Arial", 18)
    self.save_message = ""
    self.save_color = (255, 255, 255)
    self.save_status_timer = 0

  def handle_event(self, event):
    match event.type:
      case pygame.KEYDOWN if event.key == pygame.K_s:
        if self.wave_manager.is_active:
          self._show_message("Cannot save during wave!")
          return
        
        if SaveManager.save_game(self):
          self._show_message("Game saved!")
        else:
          self._show_message("Couldn't save game!")
        
      case pygame.MOUSEBUTTONDOWN if event.button == 1:
        sidebar_handled, _ = self.sidebar.handle_event(event)
        if sidebar_handled:
          return
        
        if self.selected_tower:
          self._try_place_tower(event.pos)
      
  def update(self, dt):
      if self.save_status_timer > 0:
        self.save_status_timer -= dt
        if self.save_status_timer < 0:
          self.save_status_timer = 0
          self.save_message = ""

      self.wave_manager.update(dt)
      if self.wave_manager.is_active and not self.was_wave_active:
          start_sound = Assets.sound("wavestart")
          if start_sound:
              start_sound.play()
      self.was_wave_active = self.wave_manager.is_active


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
          pop_sound = Assets.sound("balloonpop")
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
      can_place = self._can_place_tower_at(*pos)
      color = (0, 255, 0) if can_place else (255, 0, 0)

      preview = tower_factory(self.selected_tower, *pos)
      preview.draw_range(self.screen)

      preview_image = preview.image.copy()
      preview_image.set_alpha(180)
      tint = pygame.Surface(preview_image.get_size(), pygame.SRCALPHA)
      tint.fill((*color, 120))
      preview_image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

      rect = preview_image.get_rect(center=pos)
      self.screen.blit(preview_image, rect)

    if self.save_message:
      text = self.save_font.render(self.save_message, True, self.save_color)

      bg_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
      bg_rect.inflate_ip(20, 10)
      
      s = pygame.Surface((bg_rect.width, bg_rect.height))
      s.set_alpha(200)
      s.fill((0, 0, 0))
      
      self.screen.blit(s, bg_rect)
      self.screen.blit(text, text.get_rect(center=bg_rect.center))

  def _can_place_tower_at(self, x, y):
    if not self.map.can_place_tower(x, y):
      return False

    if self.selected_tower:
      preview = tower_factory(self.selected_tower, x, y)
      preview_rect = preview.image.get_rect(center=(x, y))
    else:
      preview_rect = pygame.Rect(0, 0, 32, 32)
      preview_rect.center = (x, y)

    for tower in self.towers:
      if tower.rect.colliderect(preview_rect):
        return False

    return True

  def _try_place_tower(self, pos):
    if not self._can_place_tower_at(*pos):
      return
    
    tower = tower_factory(self.selected_tower, *pos)
    if self.money < tower.COST:
      return
    
    self.towers.add(tower)
    self.money -= tower.COST
    self.selected_tower = None

  def _show_message(self, text, color=(192, 192, 192), duration=2.0):
    self.save_message = text
    self.save_color = color
    self.save_status_timer = duration