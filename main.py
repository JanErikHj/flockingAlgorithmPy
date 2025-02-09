import pygame
import quadtree
import simulation as sim
from setup import setup


BLACK = (0, 0, 0)
screen = pygame.display.set_mode((sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT))
pygame.display.set_caption("Flocking Simulation")

flock, qt = setup()

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Draw entities and add to quadtree
        for e in flock:
            e.draw(screen)
            qt.insert(quadtree.Point(e.position.x, e.position.y, data=e))

        for e in flock:
            perception = quadtree.Rectangle(e.position.x, e.position.y, sim.PERCEPTION_DISTANCE, sim.PERCEPTION_DISTANCE)
            neighbours = []
            qt.query(perception, neighbours)
            e.update(neighbours)


        # Update entities and draw them on the screen


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()