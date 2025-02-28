import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60
INITIAL_RADIUS = 10

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Canvas - Keyboard")

# Function to generate a random color
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Main game loop
def main():
    # Initial circle properties
    x, y = WIDTH // 2, HEIGHT // 2
    radius = INITIAL_RADIUS
    press_time = None
    circles = []  # Stores all circles drawn
    
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)  # Fill the screen with white background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the pressed keys
        keys = pygame.key.get_pressed()

        # Arrow keys for movement
        if keys[pygame.K_LEFT]:
            x -= 5
        if keys[pygame.K_RIGHT]:
            x += 5
        if keys[pygame.K_UP]:
            y -= 5
        if keys[pygame.K_DOWN]:
            y += 5

        # Space bar for drawing circles
        if keys[pygame.K_SPACE]:
            if press_time is None:
                press_time = time.time()  # Start timing the space bar press
            radius = int((time.time() - press_time) * 100)  # Increase size based on duration
        else:
            if press_time is not None:
                circles.append((x, y, radius, random_color()))  # Add circle on release
            press_time = None  # Reset press time when spacebar is released
            radius = INITIAL_RADIUS  # Reset to initial radius for next circle

        # Draw all circles from history
        for circle in circles:
            pygame.draw.circle(screen, circle[3], (circle[0], circle[1]), circle[2])

        # Draw the current circle preview (black outline)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 2)

        # Update the screen and maintain the frame rate
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
