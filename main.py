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

        screen_rect = self.screen.get_rect()

        self.title_text = self.title_font.render("TD Balloons", True, (0, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_rect.centerx, screen_rect.height // 4))
        
        self.start_text = self.font.render("START GAME", True, (255, 255, 255))
        self.start_rect = self.start_text.get_rect(center=screen_rect.center)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.title_text, self.title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_rect.inflate(20, 20))
        
        self.screen.blit(self.start_text, self.start_rect)

    def check_click(self, pos):
        return self.start_rect.collidepoint(pos)

class Game:
  def __init__(self, screen, clock):
    pygame.init()

    self.screen = screen
    self.clock = clock
    self.running = True

    self.map = Map(0.3)
    self.enemies = pygame.sprite.Group()
    self.towers = pygame.sprite.Group()
    self.money = 100
    self.health = 100

    self.enemies.add(balloon_factory("red", self.map.waypoints))

  def _get_events(self, event):
    match event.type:
        case pygame.QUIT:
            self.running = False
        case pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._try_place_tower(event.pos)

  def _update(self, dt):
    self.enemies.update(dt)
    for enemy in self.enemies:
      if not enemy.is_alive:
        self.money += enemy.reward
        enemy.kill()
      if enemy.has_escaped:
        self.health -= enemy.damage
        enemy.kill()

    self.towers.update(dt, self)

  def _draw(self):
    self.screen.fill((0, 0, 0))
    self.map.draw(self.screen)
    self.enemies.draw(self.screen)
    self.towers.draw(self.screen)


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
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.check_click(event.pos):
                            self.game = Game(self.screen, self.clock)
                            self.state = "GAME"
                
                elif self.state == "GAME":
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
