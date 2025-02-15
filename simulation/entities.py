import math
import random

import pygame

import simulation as sim

__all__ = ['Entity']


class Entity:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, sim.SCREEN_WIDTH), random.uniform(0, sim.SCREEN_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_x = sim.SCREEN_WIDTH
        self.max_y = sim.SCREEN_HEIGHT
        self.max_force = sim.MAX_FORCE
        self.max_turn = sim.MAX_TURN
        self.max_speed = sim.MAX_SPEED
        self.min_speed = sim.MIN_SPEED
        self.crowding_distance = sim.SEPARATION_DISTANCE
        self.acceleration = pygame.Vector2(0, 0)
        self.heading = 0.0
        self.edges = self.set_boundary(sim.EDGE_DISTANCE)

    def collision_detect(self):
        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        scale = max(left, up, right, down)

        if scale > 0:
            center = (self.max_x / 2, self.max_y / 2)
            steering = pygame.Vector2(center)
            steering -= self.position

        else:
            steering = pygame.Vector2()

        return steering

    def distance_to(self, other):
        return math.sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)

    def clamp_force(self, force: pygame.Vector2):
        if 0 < force.magnitude() < self.max_force:
            force.scale_to_length(self.max_force)

        return force

    def steering(self, neighbours):

        cohesion = pygame.Vector2()
        alignment = pygame.Vector2()
        separation = pygame.Vector2()

        for neighbour in neighbours:
            if neighbour == self:
                continue

            distance = self.position.distance_to(neighbour.position)

            # Separation
            if distance < self.crowding_distance:
                separation -= neighbour.position - self.position

            # Cohesion
            cohesion += neighbour.position

            # Alignment
            alignment += neighbour.velocity

        cohesion /= len(neighbours)
        cohesion -= self.position
        cohesion = self.clamp_force(cohesion)

        alignment /= len(neighbours)
        alignment -= self.velocity

        cohesion = self.clamp_force(cohesion)
        alignment = self.clamp_force(alignment)
        separation = self.clamp_force(separation)
        return separation / sim.SEPARATION_GAIN, alignment / sim.ALIGNMENT_GAIN, cohesion / sim.COHESION_GAIN

    def update(self, dt, neighbours):
        steering = pygame.Vector2()

        steering += self.collision_detect()

        if neighbours:
            separation, alignment, cohesion = self.steering(neighbours)
            steering += separation + alignment + cohesion

        self.acceleration = steering * dt
        # TUrn Limit
        _, old_heading = self.velocity.as_polar()
        new_velocity = self.velocity + self.acceleration * dt
        speed, new_heading = new_velocity.as_polar()

        heading_diff = 180 - (180 - new_heading + old_heading) % 360
        if abs(heading_diff) > self.max_turn:
            if heading_diff > self.max_turn:
                new_heading = old_heading + self.max_turn
            else:
                new_heading = old_heading - self.max_turn

        self.velocity.from_polar((speed, new_heading))

        speed, self.heading = self.velocity.as_polar()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt

        return self

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)

    def __str__(self):
        return "Entity(position={}, velocity={})".format(self.position, self.velocity)

    def set_boundary(self, edge_distance_pct):
        margin_w = self.max_x * edge_distance_pct / 100
        margin_h = self.max_y * edge_distance_pct / 100
        return [margin_w, margin_h, self.max_x - margin_w, self.max_y - margin_h]
