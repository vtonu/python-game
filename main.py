import pygame
import random
import math
import os
from math import sin

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 200
BACKGROUND_COLOR = (0, 0, 0)
FRAME_COLOR = (57, 255, 20)  # Neon green color

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 1
BALL_GROWTH_RATE = 0.1  # Growth rate per frame
MAX_BALL_RADIUS = 80  # Maximum ball radius before showing game over text
BALL_COLOR = (0, 255, 0)  # Green color for the ball

# Gravity settings
GRAVITY = 0.1

# Laser settings
INITIAL_LASERS = 0
MAX_LASERS = 30
LASER_INCREMENT_THRESHOLD = 2  # Ball radius increase needed to add a new laser

# Liquid effect settings
main_dir = os.path.split(os.path.abspath(__file__))[0]
imagename = os.path.join(main_dir, "data", "liquid.bmp")

try:
    liquid_bitmap = pygame.image.load(imagename)
    liquid_bitmap = pygame.transform.scale2x(liquid_bitmap)
    liquid_bitmap = pygame.transform.scale2x(liquid_bitmap)
except FileNotFoundError:
    print("File liquid.bmp not found. Please make sure it is located in the 'data' directory.")
    liquid_bitmap = pygame.Surface((20, 20))
    liquid_bitmap.fill(FRAME_COLOR)  # Fill with the same neon green color

# Load background music
pygame.mixer.music.load(os.path.join(main_dir, "data", "background.mp3"))

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Ball with Lasers")

# Font settings
font = pygame.font.SysFont('Arial', 22)

# Ball initial position and speed
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Function to draw the ball and lasers
def draw_ball_and_lasers(x, y, radius, num_lasers):
    # Draw the ball in green
    pygame.draw.circle(screen, BALL_COLOR, (x, y), radius)
    for i in range(num_lasers):
        # Draw lasers in blue-green (random choice)
        laser_color = (0, 255, 0) if random.choice([True, False]) else (0, 0, 255)
        angle = 2 * math.pi * i / num_lasers
        end_x = x + math.cos(angle) * SCREEN_WIDTH
        end_y = y + math.sin(angle) * SCREEN_HEIGHT
        pygame.draw.line(screen, laser_color, (x, y), (end_x, end_y))

# Main loop
running = True
current_lasers = INITIAL_LASERS
anim = 0.0

# Start playing background music
pygame.mixer.music.play(-1)  # -1 loops indefinitely

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if BALL_RADIUS < MAX_BALL_RADIUS:
        # Ball movement logic
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        ball_speed_y += GRAVITY

        # Ball collision with walls (no bounce sound)
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

        # Draw the liquid effect
        anim += 0.02
        int_ball_radius = int(BALL_RADIUS)  # Convert BALL_RADIUS to an integer for range
        int_ball_x = int(ball_x)  # Convert ball_x to an integer
        int_ball_y = int(ball_y)  # Convert ball_y to an integer
        xblocks = range(int_ball_x - int_ball_radius, int_ball_x + int_ball_radius, 20)
        yblocks = range(int_ball_y - int_ball_radius, int_ball_y + int_ball_radius, 20)
        for x in xblocks:
            xpos = (x + (sin(anim + x * 0.01) * 15)) + 20
            for y in yblocks:
                ypos = (y + (sin(anim + y * 0.01) * 15)) + 20
                screen.blit(liquid_bitmap, (x, y), (xpos, ypos, 20, 20))

        # Draw the frame
        pygame.draw.rect(screen, FRAME_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)

        # Draw the ball and lasers
        draw_ball_and_lasers(ball_x, ball_y, int(BALL_RADIUS), current_lasers)
    else:
        # Clear the screen and show text
        screen.fill(BACKGROUND_COLOR)
        text_surface = font.render('ChatGPT WILL TAKE YOUR JOB!', True, FRAME_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
        # Stop playing background music
        pygame.mixer.music.stop()

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()