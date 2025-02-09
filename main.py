import pygame

import quadtree
import simulation as sim
from setup import setup

BLACK = (0, 0, 0)


def main():
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT))
    pygame.display.set_caption("Flocking Simulation")
    flock, qt = setup()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        # Clear points from quadtree
        qt.clear()

        # Draw entities and add to empty quadtree
        for e in flock:
            e.draw(screen)
            qt.insert(quadtree.Point(e.position.x, e.position.y, data=e))

        # Update all entities
        for e in flock:
            perception = quadtree.Rectangle(e.position.x, e.position.y, sim.PERCEPTION_DISTANCE,
                                            sim.PERCEPTION_DISTANCE)
            neighbours = []
            qt.query(perception, neighbours)
            e.update([n.data for n in neighbours])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
