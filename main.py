import pygame
from settings import *
from map import Map
from balloons import balloon_factory
from towers import tower_factory

class Menu:
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

    def handle_click(self, pos):
        if self.state == "MAIN":
            if self.start_rect.collidepoint(pos):
                self.state = "DIFFICULTY"
                return None
        elif self.state == "DIFFICULTY":
            for text, rect, level in self.level_buttons:
                if rect.collidepoint(pos):
                    return level
        return None

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

    self.enemies.add(balloon_factory("yellow", self.map.waypoints, self.difficulty))

  def _get_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._try_place_tower(event.pos)

  def _update(self, dt):
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

  def _try_place_tower(self, pos):
    if not self.map.can_place_tower(*pos):
      return
    
    tower = tower_factory("basic", *pos)

    if self.money < tower.COST:
      return
    if pygame.sprite.spritecollideany(tower, self.towers):
      return
    
    self.towers.add(tower)
    self.money -= tower.COST

class MainManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TD Balloons")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "MENU"
        self.menu = Menu(self.screen)
        self.game = None

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        selected_diff = self.menu.handle_click(event.pos)
                        if selected_diff:
                            self.game = Game(self.screen, self.clock, selected_diff)
                            self.state = "GAME"
                
                elif self.state == "GAME":
                    if self.game:
                        self.game._get_events(event)

            if self.state == "MENU":
                self.menu.draw()
            elif self.state == "GAME":
                if self.game:
                    self.game._update(dt)
                    self.game._draw()
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    manager = MainManager()
    manager.run()
