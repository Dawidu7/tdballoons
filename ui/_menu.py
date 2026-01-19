import pygame
from states import GameState

class Menu(GameState):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 64)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.state = "MAIN"

        screen_rect = self.screen.get_rect()

        self.title_text = self.title_font.render("TD Balloons", True, (0, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_rect.centerx, 150))
        
        self.start_text = self.font.render("NEW GAME", True, (255, 255, 255))
        self.start_rect = self.start_text.get_rect(center=screen_rect.center)
        
        self.diff_title = self.font.render("SELECT DIFFICULTY", True, (255, 255, 0))
        self.diff_title_rect = self.diff_title.get_rect(center=(screen_rect.centerx, 200))

        self.levels = ["Easy", "Normal", "Hard"]
        self.level_buttons = []
        for i, level in enumerate(self.levels):
            text = self.font.render(level, True, (255, 255, 255))
            rect = text.get_rect(center=(screen_rect.centerx, 350 + i * 100))
            self.level_buttons.append((text, rect, level))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "MAIN":
            self.screen.blit(self.title_text, self.title_rect)
            if self.start_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 100), self.start_rect.inflate(20, 20))
            self.screen.blit(self.start_text, self.start_rect)
            
        elif self.state == "DIFFICULTY":
            self.screen.blit(self.diff_title, self.diff_title_rect)
            for text, rect, level in self.level_buttons:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (100, 100, 100), rect.inflate(20, 20))
                self.screen.blit(text, rect)

    def _handle_click(self, pos):
        if self.state == "MAIN":
            if self.start_rect.collidepoint(pos):
                self.state = "DIFFICULTY"
                return None
        elif self.state == "DIFFICULTY":
            for _, rect, level in self.level_buttons:
                if rect.collidepoint(pos):
                    return level
        return None