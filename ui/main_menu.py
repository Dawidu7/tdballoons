import pygame
from core.save_manager import SaveManager
from settings import WIDTH, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR
from states import GameState
from .button import Button

class MainMenu(GameState):
  def __init__(self, manager):
    self.manager = manager

    self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
    self.btn_font = pygame.font.SysFont("Arial", 64)

    self.title_text = self.title_font.render("TD Balloons", True, (0, 255, 255))
    self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, 150))

    self.buttons = [
      Button(
        text="NEW GAME",
        pos=(WIDTH // 2, 300),
        font=self.btn_font,
        bg_color=MENU_BUTTON_COLOR,
        hover_color=(0, 180, 0),
        action=self.manager.go_to_difficulty
      ),
      Button(
        text="CONTINUE",
        pos=(WIDTH // 2, 450),
        font=self.btn_font,
        bg_color=MENU_BUTTON_COLOR,
        hover_color=MENU_BUTTON_HOVER_COLOR,
        action=self._load_game
      ) if SaveManager.has_save() else None,
      Button(
        text="QUIT",
        pos=(WIDTH // 2, 600 if SaveManager.has_save() else 450),
        font=self.btn_font,
        bg_color=MENU_BUTTON_COLOR,
        hover_color=MENU_BUTTON_HOVER_COLOR,
        action=self._quit_game
      ),
    ]

  def handle_event(self, event):
    for button in self.buttons:
      if button:
        button.handle_event(event)

  def update(self, dt):
    pass

  def draw(self):
    self.manager.screen.fill((30, 30, 30))

    self.manager.screen.blit(self.title_text, self.title_rect)

    for button in self.buttons:
      if button:
        button.draw(self.manager.screen)

  def _quit_game(self):
    pygame.event.post(pygame.event.Event(pygame.QUIT))

  def _load_game(self):
    data = SaveManager.load_game()
    if data:
      self.manager.go_to_game(save_data=data)