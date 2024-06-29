import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 200
BACKGROUND_COLOR = (0, 0, 0)
FRAME_COLOR = (57, 255, 20)  # Neon green color

# Ball settings
BALL_RADIUS = 15
BALL_COLOR = (57, 255, 20)  # Neon green color
BALL_SPEED = 5
BALL_GROWTH_RATE = 0.1  # Growth rate per frame
MAX_BALL_RADIUS = 60  # Maximum ball radius before showing "GOOD SHIT"

# Gravity settings
GRAVITY = 0.5

# Laser settings
INITIAL_LASERS = 0
MAX_LASERS = 30
LASER_INCREMENT_THRESHOLD = 2  # Ball radius increase needed to add a new laser

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Ball with Lasers")

# Font settings
font = pygame.font.SysFont('Arial', 28)

# Ball initial position and speed
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Function to draw the ball and lasers
def draw_ball_and_lasers(x, y, radius, num_lasers):
    pygame.draw.circle(screen, BALL_COLOR, (x, y), radius)
    for i in range(num_lasers):
        angle = 2 * math.pi * i / num_lasers
        end_x = x + math.cos(angle) * SCREEN_WIDTH
        end_y = y + math.sin(angle) * SCREEN_HEIGHT
        pygame.draw.line(screen, FRAME_COLOR, (x, y), (end_x, end_y))

# Main loop
running = True
current_lasers = INITIAL_LASERS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if BALL_RADIUS < MAX_BALL_RADIUS:
        # Ball movement logic
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        ball_speed_y += GRAVITY

        # Ball collision with walls
        if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y - BALL_RADIUS < 0 or ball_y + BALL_RADIUS > SCREEN_HEIGHT:
            ball_speed_y = -ball_speed_y

        # Ball growth
        BALL_RADIUS += BALL_GROWTH_RATE

        # Increase the number of lasers as the ball grows
        if BALL_RADIUS // LASER_INCREMENT_THRESHOLD > current_lasers and current_lasers < MAX_LASERS:
            current_lasers += 1

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the frame
        pygame.draw.rect(screen, FRAME_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)

        # Draw the ball and lasers
        draw_ball_and_lasers(ball_x, ball_y, int(BALL_RADIUS), current_lasers)
    else:
        # Clear the screen and show text
        screen.fill(BACKGROUND_COLOR)
        text_surface = font.render('ChatGPT Will Take Your Job!', True, FRAME_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()