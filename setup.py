import pygame
import quadtree
import simulation as sim

def setup():
    flock = [sim.Entity for _ in range(sim.NUM_ENTITIES)]
    area = quadtree.Rectangle(sim.SCREEN_WIDTH/2, sim.SCREEN_HEIGHT/2, sim.SCREEN_WIDTH/2, sim.SCREEN_HEIGHT/2)
    qt = quadtree.QuadTree(area, 4)
    return flock, qt

