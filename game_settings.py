import pygame
import random
import math
import os
from math import sin

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
FRAME_COLOR = (57, 255, 20)  # Neon green color

# Ball settings
BALL_RADIUS = 0.9
BALL_SPEED = 10
BALL_GROWTH_RATE = 0.01  # Growth rate per frame
MAX_BALL_RADIUS = 10  # Maximum ball radius before showing game over text
BALL_COLOR = (0, 255, 0)  # Green color for the ball

# Gravity settings
GRAVITY = 2

# Laser settings
INITIAL_LASERS = 1
MAX_LASERS = 5

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

    # Calculate distances to corners of the window
    top_left_dist = math.sqrt(x**2 + y**2)
    top_right_dist = math.sqrt((SCREEN_WIDTH - x)**2 + y**2)
    bottom_left_dist = math.sqrt(x**2 + (SCREEN_HEIGHT - y)**2)
    bottom_right_dist = math.sqrt((SCREEN_WIDTH - x)**2 + (SCREEN_HEIGHT - y)**2)

    for i in range(num_lasers):
        # Calculate angle for each laser
        angle = 2 * math.pi * i / num_lasers

        # Calculate end point coordinates for blue lasers
        end_x_blue = x + math.cos(angle) * radius * 1.7  # Adjust multiplier as needed
        end_y_blue = y + math.sin(angle) * radius * 1.7  # Adjust multiplier as needed
        pygame.draw.line(screen, (0, 0, 255), (x, y), (int(end_x_blue), int(end_y_blue)))

        # Calculate end point coordinates for green lasers (twice the length of blue lasers)
        end_x_green = x + math.cos(angle) * radius * 3
        end_y_green = y + math.sin(angle) * radius * 3
        pygame.draw.line(screen, (0, 255, 0), (x, y), (int(end_x_green), int(end_y_green)))