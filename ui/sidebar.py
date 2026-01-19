import pygame
from .button import Button
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH

class Sidebar:
  def __init__(self, game, towers):
    self.game = game
    
    self.rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    self.font = pygame.font.SysFont("Arial", 24)
    self.font_small = pygame.font.SysFont("Arial", 18)

    self.start_wave_button = Button(
      text="Start Wave 1",
      pos=(self.rect.x + self.rect.width // 2, 145),
      font=self.font_small,
      bg_color=(80, 120, 80),
      hover_color=(100, 140, 100),
      action=self.game.wave_manager.start_next_wave
    )

    self.tower_buttons = []
    start_y, spacing = 200, 80
    for i, (name, cost) in enumerate(towers):
      btn = Button(
        text=f"{name.title()} ${cost}",
        pos=(self.rect.centerx, start_y + i * spacing),
        font=self.font_small,
        bg_color=(80, 80, 80),
        hover_color=(100, 100, 100),
        action=lambda n=name: self._select_tower(n)
      )
      btn.cost = cost
      btn.name = name

      self.tower_buttons.append(btn)

  def handle_event(self, event):
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
      return False
    
    if not self.rect.collidepoint(event.pos):
      return False
    
    if not self.game.wave_manager.is_active and self.start_wave_button.handle_event(event):
      return True
    
    for btn in self.tower_buttons:
      if self.game.money >= btn.cost:
        if btn.handle_event(event):
          return True
      
    return True

  def draw(self, screen):
    pygame.draw.rect(screen, (40, 40, 40), self.rect)
    screen.blit(self.font.render(f"HP: {self.game.hp}", True, (255, 255, 255)), (self.rect.x + 20, 20))
    screen.blit(self.font.render(f"Money: {self.game.money}", True, (255, 255, 255)), (self.rect.x + 20, 60))

    if self.game.wave_manager.is_active:
      self.start_wave_button.bg_color = (120, 120, 120)
      self.start_wave_button.hover_color = (120, 120, 120)
      self.start_wave_button.set_text("Wave Active")
    else:
      self.start_wave_button.bg_color = (80, 120, 80)
      self.start_wave_button.hover_color = (100, 140, 100)
      self.start_wave_button.set_text(f"Start Wave {self.game.wave_manager.wave + 1}")

    self.start_wave_button.draw(screen)

    for btn in self.tower_buttons:
      btn.draw(screen)
  
  def _select_tower(self, name):
    self.game.selected_tower = name