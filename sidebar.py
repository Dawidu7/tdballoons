import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SIDEBAR_WIDTH

class Sidebar:
  def __init__(self):
    self.rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    self.font = pygame.font.SysFont("Arial", 24)
    self.small = pygame.font.SysFont("Arial", 18)
    self.buttons = []
    self.selected = None

  def set_buttons(self, tower_defs):
    self.buttons.clear()
    x = self.rect.x + 20
    y = 200
    for name, cost in tower_defs:
      btn = pygame.Rect(x, y, self.rect.width - 40, 50)
      self.buttons.append((btn, name, cost))
      y += 70

  def draw(self, surface, hp, money):
    pygame.draw.rect(surface, (40, 40, 40), self.rect)
    surface.blit(self.font.render(f"HP: {hp}", True, (255, 255, 255)), (self.rect.x + 20, 20))
    surface.blit(self.font.render(f"Money: {money}", True, (255, 255, 255)), (self.rect.x + 20, 60))

    for btn, name, cost in self.buttons:
      color = (80, 120, 80) if self.selected == name else (80, 80, 80)
      pygame.draw.rect(surface, color, btn)
      surface.blit(self.small.render(f"{name.title()} (${cost})", True, (255, 255, 255)), (btn.x + 10, btn.y + 14))

  def handle_click(self, pos):
    if not self.rect.collidepoint(pos):
      return None
    for btn, name, _ in self.buttons:
      if btn.collidepoint(pos):
        self.selected = name
        return name
    return None