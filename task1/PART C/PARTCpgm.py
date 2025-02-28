import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60
circle_radius = 10  # Initial circle radius
circle_x, circle_y = WIDTH // 2, HEIGHT // 2  # Starting position in the center
press_time = None  # To track how long the space bar is held down

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Canvas with Path and Cleanup")

# Function to generate a random color
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to save the screen as an image
def save_image():
    pygame.image.save(screen, "drawing.png")
    print("Drawing saved as 'drawing.png'")

# Main function
def main():
    global circle_x, circle_y, circle_radius, press_time
    running = True
    clock = pygame.time.Clock()
    circles = []  # List to hold circle data
    total_path_length = 0  # Variable to store the total path length

    while running:
        screen.fill(WHITE)  # Fill screen with white background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Right-click to remove the last circle
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right-click
                    if circles:
                        circles.pop()  # Remove the last circle
                        total_path_length = 0  # Reset path length
                        # Recalculate path length for remaining circles
                        for i in range(1, len(circles)):
                            last_circle = circles[i - 1]
                            total_path_length += calculate_distance(last_circle[0], last_circle[1], circles[i][0], circles[i][1])

            # Space bar to clear the canvas
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space bar pressed
                    circles.clear()  # Clear all circles
                    total_path_length = 0  # Reset the path length
                elif event.key == pygame.K_s:  # Press 'S' to save the drawing
                    save_image()

        # Check for arrow keys to move the circle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            circle_x -= 5
        if keys[pygame.K_RIGHT]:
            circle_x += 5
        if keys[pygame.K_UP]:
            circle_y -= 5
        if keys[pygame.K_DOWN]:
            circle_y += 5

        # Check for spacebar to start drawing
        if keys[pygame.K_SPACE]:  # Space bar is held down
            if press_time is None:
                press_time = time.time()  # Record the press time
            circle_radius = int((time.time() - press_time) * 100)  # Increase size with hold duration
        else:
            if press_time is not None:
                circles.append((circle_x, circle_y, circle_radius, random_color()))  # Add circle on release
                # If there are multiple circles, calculate and add the path length
                if len(circles) > 1:
                    last_circle = circles[-2]  # The previous circle
                    total_path_length += calculate_distance(last_circle[0], last_circle[1], circle_x, circle_y)

            press_time = None  # Reset press time when spacebar is released
            circle_radius = 10  # Reset to default size for the next circle

        # Draw all the circles
        for circle in circles:
            pygame.draw.circle(screen, circle[3], (circle[0], circle[1]), circle[2])

        # Draw the current circle preview
        pygame.draw.circle(screen, (0, 0, 0), (circle_x, circle_y), circle_radius, 2)  # Circle preview in black

        # Draw lines connecting the consecutive circles
        for i in range(1, len(circles)):
            pygame.draw.line(screen, (0, 0, 0), (circles[i-1][0], circles[i-1][1]), (circles[i][0], circles[i][1]), 2)

        # Display the total path length
        font = pygame.font.SysFont(None, 30)
        path_length_text = font.render(f"Total Path Length: {total_path_length:.2f} pixels", True, (0, 0, 0))
        screen.blit(path_length_text, (10, HEIGHT - 30))  # Display at bottom left

        pygame.display.flip()  # Update the screen
        clock.tick(FPS)  # Maintain 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

