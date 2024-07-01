import pygame
import random
import math
from math import sin
from game_settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FRAME_COLOR,
    BALL_RADIUS, BALL_SPEED, BALL_GROWTH_RATE, MAX_BALL_RADIUS, BALL_COLOR,
    GRAVITY, INITIAL_LASERS, MAX_LASERS, LASER_INCREMENT_THRESHOLD, 
    liquid_bitmap, screen, font, ball_x, ball_y, ball_speed_x, ball_speed_y,
    draw_ball_and_lasers
)

# Main loop
running = True
current_lasers = INITIAL_LASERS
anim = 0.0

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
        draw_ball_and_lasers(screen, ball_x, ball_y, int(BALL_RADIUS), current_lasers)
    else:
        # Clear the screen and show text
        screen.fill(BACKGROUND_COLOR)
        text_surface = font.render('AI Will Take Your Job!', True, FRAME_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()