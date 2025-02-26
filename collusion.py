import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Collision Detection with Effect')

# Define object properties
rect1 = pygame.Rect(100, 100, 50, 50)  # x, y, width, height
rect2 = pygame.Rect(300, 200, 50, 50)  # x, y, width, height

# Movement speed
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Handle key presses for moving rect1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect1.x -= speed
    if keys[pygame.K_RIGHT]:
        rect1.x += speed
    if keys[pygame.K_UP]:
        rect1.y -= speed
    if keys[pygame.K_DOWN]:
        rect1.y += speed

    # Check for collision
    collision = rect1.colliderect(rect2)

    # Fill the screen with white
    screen.fill(white)

    # Draw the rectangles
    if collision:
        pygame.draw.rect(screen, red, rect1)
        pygame.draw.rect(screen, red, rect2)
    else:
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
