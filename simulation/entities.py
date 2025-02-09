import math
import random

import pygame

import simulation as sim


__all__ = ['Entity']


class Entity:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, sim.SCREEN_WIDTH), random.uniform(0, sim.SCREEN_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))

    def collision_detect(self):
        if self.position.x < 0 or self.position.x > sim.SCREEN_WIDTH:
            self.velocity.reflect_ip(self.velocity.project(pygame.Vector2(1, 0)))

        if self.position.y < 0 or self.position.y > sim.SCREEN_HEIGHT:
            self.velocity.reflect_ip(self.velocity.project(pygame.Vector2(0, 1)))

        self.velocity.scale_to_length(sim.MAX_SPEED)


    def distance_to(self, other):
        return math.sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)

    def update(self, neighbours):
        if len(neighbours) == 0:
            self.collision_detect()
            self.position += self.velocity

            return

        cohesion = pygame.Vector2(0, 0)
        alignment = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)

        for neighbour in neighbours:
            if neighbour == self:
                continue

            distance = self.distance_to(neighbour)
            cohesion += neighbour.position * (1/distance)
            alignment += neighbour.velocity * (1/distance)


            if distance < sim.SEPARATION_DISTANCE:
                separation += neighbour.position * (1/distance)

        self.velocity += (cohesion / len(neighbours)) #* sim.COHESION_GAIN
        self.velocity += (alignment / len(neighbours)) #* sim.ALIGNMENT_GAIN
        self.velocity -= (separation / len(neighbours)) #* sim.SEPARATION_GAIN
        self.velocity.scale_to_length(sim.MAX_SPEED)
        self.collision_detect()
        self.position += self.velocity


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)

    def __str__(self):
        return "Entity(position={}, velocity={})".format(self.position, self.velocity)
