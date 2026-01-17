import pygame
from abc import ABC, abstractmethod

class Balloon(pygame.sprite.Sprite):
    def __init__(self, hp, speed, damage, reward, path):
        super().__init__()

        mults = multipliers if multipliers else {"hp_mult": 1.0, "speed_mult": 1.0, "reward_mult": 1.0}

        self.hp = hp * mults["hp_mult"]
        self.speed = speed * mults["speed_mult"]
        self.reward = int(reward * mults["reward_mult"])
        self.damage = damage
        self.path = path # Placeholder na punkty sciezki
        self.current_point_index = 0 # Licznik do punktu do ktorego sie udaje na sciezce
        self.child_type = child_type # Okreslenie na jaki balon rozpada sie po smierci
        
        # self.image = pygame.image.load("*.png").convert_alpha()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        
        if self.path:
            self.rect.center = self.path[0]

    @abstractmethod
    def move(self):
        if self.current_point_index < len(self.path) - 1:
            target = pygame.Vector2(self.path[self.current_point_index + 1])
            current = pygame.Vector2(self.rect.center)

            pass

    def update(self):
        self.move()