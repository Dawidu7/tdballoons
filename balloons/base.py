import pygame

class Balloon(pygame.sprite.Sprite):
    def __init__(self, hp, speed, damage, reward, waypoints):
        super().__init__()

        self.hp = hp
        self.speed = speed * 100
        self.reward = reward
        self.damage = damage
        self.waypoints = waypoints
        self.current_waypoint_index = 0
        
        # self.image = pygame.image.load("*.png").convert_alpha()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        
        self.pos = pygame.Vector2(self.waypoints[0])
        self.rect.center = self.pos

    @property
    def is_alive(self):
        return self.hp > 0
    
    def update(self, dt):
        self.move(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dt):
        if self.current_waypoint_index >= len(self.waypoints) - 1:
            return
        
        target = pygame.Vector2(self.waypoints[self.current_waypoint_index + 1])
        direction = target - self.pos
        distance = direction.length()

        if distance == 0:
            self.current_waypoint_index += 1
            return
        
        step = self.speed * dt
        if distance <= step:
            self.pos = target
            self.current_waypoint_index += 1
        else:
            self.pos += direction.normalize() * step

        self.rect.center = self.pos
