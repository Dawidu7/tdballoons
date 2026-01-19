import pygame

class Button:
  def __init__(self, text, pos, font, bg_color, hover_color, action, disabled_color=(60, 60, 60), text_color=(255, 255, 255), disabled_text_color=(180, 180, 180)):
    self.pos = pos
    self.font = font
    self.bg_color = bg_color
    self.hover_color = hover_color
    self.disabled_color = disabled_color
    self.text_color = text_color
    self.disabled_text_color = disabled_text_color
    self.action = action
    self.is_disabled = False

    self.set_text(text)

  def set_text(self, text):
    if text == getattr(self, "text", None):
      return

    self.text = text
    color = self.disabled_text_color if self.is_disabled else self.text_color
    self.text_surf = self.font.render(self.text, True, color)
    self.rect = self.text_surf.get_rect(center=self.pos)
    self.bg_rect = self.rect.inflate(30, 20)

  def handle_event(self, event):
    if self.is_disabled:
      return False
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self._is_hovered(event.pos):
        self.action()
        return True
    return False
  
  def draw(self, screen):
    if self.is_disabled:
      color = self.disabled_color
    else:
      color = self.hover_color if self._is_hovered() else self.bg_color

    color_text = self.disabled_text_color if self.is_disabled else self.text_color
    if self.text_surf.get_at((0, 0))[:3] != color_text:
      self.text_surf = self.font.render(self.text, True, color_text)
      self.rect = self.text_surf.get_rect(center=self.pos)
      self.bg_rect = self.rect.inflate(30, 20)

    pygame.draw.rect(screen, color, self.bg_rect, border_radius=10)
    screen.blit(self.text_surf, self.rect)

  def _is_hovered(self, pos=None):
    return self.bg_rect.collidepoint(pos if pos else pygame.mouse.get_pos())