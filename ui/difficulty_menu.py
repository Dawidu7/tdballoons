import pygame
from settings import WIDTH, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR
from states import GameState
from .button import Button

class DifficultyMenu(GameState):
  def __init__(self, manager):
    self.manager = manager

    self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
    self.btn_font = pygame.font.SysFont("Arial", 64)

    self.title_text = self.title_font.render("SELECT DIFFICULTY", True, (255, 255, 0))
    self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, 200))

    difficulties = ["easy", "normal", "hard"]
    self.buttons = [
      Button(
        text=difficulty.capitalize(),
        pos=(WIDTH // 2, 300 + 150 * i),
        font=self.btn_font,
        bg_color=MENU_BUTTON_COLOR,
        hover_color=MENU_BUTTON_HOVER_COLOR,
        action=lambda: self.manager.go_to_game(difficulty=difficulty)
      ) for i, difficulty in enumerate(difficulties)
    ]

  def handle_event(self, event):
    for button in self.buttons:
      button.handle_event(event)

  def update(self, dt):
    pass

  def draw(self):
    self.manager.screen.fill((30, 30, 30))

    self.manager.screen.blit(self.title_text, self.title_rect)

    for button in self.buttons:
      button.draw(self.manager.screen)