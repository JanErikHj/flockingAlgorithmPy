import vector
import random
import math
import pygame
import simulation.simulationParameters as sp

__all__ = ['Entity']

class Entity:
    def __init__(self):
        self.position = vector.obj(x = random.uniform(0, sp.SCREEN_WIDTH), y = random.uniform(0, sp.SCREEN_HEIGHT))
        self.velocity = vector.obj(x = random.uniform(-3, 3), y = random.uniform(-3, 3))

    def collision_detect(self):
        pass

    def distance_to(self, other):
        return math.sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)

    def update(self, flock):
        pass




    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)
