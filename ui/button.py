import pygame

class Button:
  def __init__(self, text, pos, font, bg_color, hover_color, action):
    self.pos = pos
    self.font = font
    self.bg_color = bg_color
    self.hover_color = hover_color
    self.action = action

    self.set_text(text)

  def set_text(self, text):
    self.text = text
    self.text_surf = self.font.render(self.text, True, (255, 255, 255))
    self.rect = self.text_surf.get_rect(center=self.pos)
    self.bg_rect = self.rect.inflate(30, 20)

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self._is_hovered(event.pos):
        self.action()
        return True
    return False
  
  def draw(self, screen):
    color = self.hover_color if self._is_hovered() else self.bg_color

    pygame.draw.rect(screen, color, self.bg_rect, border_radius=10)
    screen.blit(self.text_surf, self.rect)

  def _is_hovered(self, pos=None):
    return self.bg_rect.collidepoint(pos if pos else pygame.mouse.get_pos())