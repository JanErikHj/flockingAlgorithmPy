import pygame
import quadtree
import simulation as sim


BLACK = (0, 0, 0)
screen = pygame.display.set_mode((sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT))
pygame.display.set_caption("Flocking Simulation")



def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update entities and draw them on the screen
        screen.fill(BLACK)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()