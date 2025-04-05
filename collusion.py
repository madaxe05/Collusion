import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('60-Second Collision Challenge')

# Initialize sound
pygame.mixer.init()
try:
    collision_sound = pygame.mixer.Sound("/Users/sohandhungel/Desktop/project/cg/rough/collusion/209018__owlstorm__fruit-impact-3.wav")
except:
    # Create a silent sound if file not found
    collision_sound = pygame.mixer.Sound(buffer=bytearray(44))

# Define open-path obstacles (no closed boxes)
fixed_obstacles = [
    # Vertical obstacles (leave gaps between them)
    pygame.Rect(150, 100, 30, 200),
    pygame.Rect(150, 400, 30, 150),
    pygame.Rect(350, 50, 30, 200),
    pygame.Rect(350, 350, 30, 200),
    pygame.Rect(550, 100, 30, 200),
    pygame.Rect(550, 400, 30, 150),
    
    # Horizontal obstacles (leave gaps between them)
    pygame.Rect(50, 200, 200, 30),
    pygame.Rect(300, 200, 200, 30),
    pygame.Rect(550, 200, 200, 30),
    pygame.Rect(50, 400, 200, 30),
    pygame.Rect(300, 400, 200, 30),
    pygame.Rect(550, 400, 200, 30),
    
    # Some diagonal-like obstacles (not fully closed)
    pygame.Rect(200, 300, 100, 30),
    pygame.Rect(500, 300, 100, 30),
]

# Define object properties
player_rect = pygame.Rect(50, 50, 20, 20)  # Player rectangle
target_rect = pygame.Rect(400, 300, 20, 20) # Target rectangle

# Movement speed (slow)
speed = 2
velocity = 0
acceleration = 0.05

# Game variables
score = 0
collision_cooldown = 0
game_start_time = time.time()
game_duration = 60  # 60 seconds
game_active = True
game_result = ""
waiting_for_restart = False

# Font setup
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

def keep_in_bounds(rect):
    if rect.left < 0:
        rect.left = 0
    if rect.right > screen_width:
        rect.right = screen_width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > screen_height:
        rect.bottom = screen_height

def handle_movement(rect):
    global velocity
    
    # Store old position
    old_x, old_y = rect.x, rect.y
    
    # Apply movement with reduced acceleration
    velocity = min(velocity + acceleration, speed)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect.x -= velocity
    if keys[pygame.K_RIGHT]:
        rect.x += velocity
    if keys[pygame.K_UP]:
        rect.y -= velocity
    if keys[pygame.K_DOWN]:
        rect.y += velocity
    
    # Precise collision detection with obstacles
    for obstacle in fixed_obstacles:
        if rect.colliderect(obstacle):
            # Try moving back just on X axis
            rect.x = old_x
            if rect.colliderect(obstacle):
                # If still colliding, try moving back just on Y axis
                rect.x, rect.y = old_x, old_y
                rect.y = old_y
                if rect.colliderect(obstacle):
                    # If still colliding, revert completely
                    rect.x, rect.y = old_x, old_y
            break
    
    # Keep player within screen bounds
    keep_in_bounds(rect)

def respawn_target():
    """Respawn target at a random location that doesn't collide with obstacles"""
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        new_x = random.randint(20, screen_width - 40)
        new_y = random.randint(20, screen_height - 40)
        target_rect.x = new_x
        target_rect.y = new_y
        
        # Check if new position collides with any obstacle
        valid_position = True
        for obstacle in fixed_obstacles:
            if target_rect.colliderect(obstacle):
                valid_position = False
                break
        
        if valid_position:
            return
    
    # Fallback position if no valid spot found
    target_rect.x = screen_width // 2
    target_rect.y = screen_height // 2

def check_collision():
    global score, collision_cooldown, game_result, game_active, waiting_for_restart
    
    # Precise collision detection between player and target
    if (abs(player_rect.centerx - target_rect.centerx) < (player_rect.width/2 + target_rect.width/2) and
       abs(player_rect.centery - target_rect.centery) < (player_rect.height/2 + target_rect.height/2)):
        if collision_cooldown <= 0:
            score += 1
            collision_cooldown = 30
            collision_sound.play()
            respawn_target()
    elif collision_cooldown > 0:
        collision_cooldown -= 1
    
    # Check game time
    elapsed_time = time.time() - game_start_time
    remaining_time = max(0, game_duration - elapsed_time)
    
    if remaining_time <= 0 and game_active:
        game_active = False
        waiting_for_restart = True
        game_result = "You Win!" if score >= 10 else "You Lose!"
    
    return remaining_time

def draw_game_objects(remaining_time):
    screen.fill(white)
    
    # Draw obstacles (green)
    for obstacle in fixed_obstacles:
        pygame.draw.rect(screen, green, obstacle)
    
    # Draw player (red) and target (blue)
    pygame.draw.rect(screen, red, player_rect)
    pygame.draw.rect(screen, blue, target_rect)
    
    # Draw score and time
    score_text = font_small.render(f"Score: {score}", True, black)
    time_text = font_small.render(f"Time: {int(remaining_time)}s", True, black)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (screen_width - 150, 10))
    
    # Draw game over message if game ended
    if waiting_for_restart:
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        result_text = font_large.render(game_result, True, yellow)
        final_score_text = font_medium.render(f"Final Score: {score}", True, white)
        restart_text = font_small.render("Press SPACE to play again or Q to quit", True, white)
        
        screen.blit(result_text, (screen_width//2 - result_text.get_width()//2, screen_height//2 - 100))
        screen.blit(final_score_text, (screen_width//2 - final_score_text.get_width()//2, screen_height//2))
        screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 100))
    
    pygame.display.flip()

def reset_game():
    global score, game_start_time, game_active, game_result, player_rect, waiting_for_restart
    
    score = 0
    game_start_time = time.time()
    game_active = True
    game_result = ""
    waiting_for_restart = False
    
    # Reset player position
    player_rect.x = 50
    player_rect.y = 50
    
    # Respawn target
    respawn_target()

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if waiting_for_restart:
                if event.key == pygame.K_SPACE:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False

    if game_active:
        # Handle movement for player
        handle_movement(player_rect)
        
        # Check for collisions and update game state
        remaining_time = check_collision()
    else:
        remaining_time = 0
    
    # Draw everything
    draw_game_objects(remaining_time)
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()