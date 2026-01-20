import pygame
import os
from assets import Assets

class Balloon(pygame.sprite.Sprite):
    def __init__(self, color_name, hp, speed, damage, reward, waypoints, current_waypoint, current_pos=None):
        super().__init__()
        
        self.hp = hp
        self.speed = speed * 100 
        self.reward = reward
        self.damage = damage
        self.waypoints = waypoints
        self.current_waypoint_index = current_waypoint
        self.child_type = None 

        key = f"balloons.{color_name}"
        img = Assets.image(key, (40, 50))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 255))
            
        self.rect = self.image.get_rect()
        self.pos = current_pos if current_pos else pygame.Vector2(self.waypoints[0])
        self.rect.center = self.pos

    @property
    def is_alive(self):
        return self.hp > 0
    
    @property
    def has_escaped(self):
        return self.current_waypoint_index >= len(self.waypoints) - 1
    
    def update(self, dt):
        self.move(dt)

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

    def take_damage(self, damage):
        self.hp -= damage
