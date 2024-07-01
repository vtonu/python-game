import pygame
import random
import math
import os
from math import sin

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
FRAME_COLOR = (57, 255, 20)  # Neon green color

# Ball settings
BALL_RADIUS = 5
BALL_SPEED = 1
BALL_GROWTH_RATE = 0.01  # Growth rate per frame
MAX_BALL_RADIUS = 10  # Maximum ball radius before showing game over text
BALL_COLOR = (0, 255, 0)  # Green color for the ball

# Gravity settings
GRAVITY = 0.8

# Laser settings
INITIAL_LASERS = 0
MAX_LASERS = 100

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

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball with Lasers")

# Font settings
font = pygame.font.SysFont('Arial', 22)

# Ball initial position and speed
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

def draw_ball_and_lasers(screen, x, y, radius, num_lasers):
    # Draw the ball in green
    pygame.draw.circle(screen, BALL_COLOR, (x, y), radius)
    for i in range(num_lasers):
        # Draw lasers in blue-green (random choice)
        laser_color = (0, 255, 0) if random.choice([True, False]) else (0, 0, 255)
        angle = 2 * math.pi * i / num_lasers
        end_x = x + math.cos(angle) * SCREEN_WIDTH
        end_y = y + math.sin(angle) * SCREEN_HEIGHT
        pygame.draw.line(screen, laser_color, (x, y), (end_x, end_y))