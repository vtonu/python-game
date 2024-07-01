import pygame
import random
import math
from math import sin
from game_settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FRAME_COLOR,
    BALL_RADIUS, BALL_SPEED, BALL_GROWTH_RATE, MAX_BALL_RADIUS, BALL_COLOR,
    GRAVITY, INITIAL_LASERS, MAX_LASERS, 
    liquid_bitmap, screen, font, ball_x, ball_y, ball_speed_x, ball_speed_y,
    draw_ball_and_lasers
)

def draw_button(screen, text, x, y, width, height, border_color, text_color):
    pygame.draw.rect(screen, border_color, (x, y, width, height), 3)
    button_font = pygame.font.SysFont('Arial', 18)  # Use a smaller font size
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def is_button_clicked(mouse_pos, x, y, width, height):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, current_lasers, ball_radius
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = BALL_SPEED
    ball_speed_y = BALL_SPEED
    current_lasers = INITIAL_LASERS
    ball_radius = BALL_RADIUS

# Main loop
running = True
current_lasers = INITIAL_LASERS
anim = 0.0
ball_radius = BALL_RADIUS  # Local variable for ball radius

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if is_button_clicked(mouse_pos, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 40, 100, 40):
                reset_game()

    if ball_radius < MAX_BALL_RADIUS:
        # Ball movement logic
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        ball_speed_y += GRAVITY

        # Ball collision with walls (no bounce sound)
        if ball_x - ball_radius < 0 or ball_x + ball_radius > SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y + ball_radius > SCREEN_HEIGHT:
            ball_speed_y = -ball_speed_y

            # Increase the number of lasers as the ball bounces on the ground
            if current_lasers < MAX_LASERS:
                current_lasers += 1

        # Prevent the ball from going above the top of the screen
        if ball_y - ball_radius < 0:
            ball_y = ball_radius
            ball_speed_y = GRAVITY

        # Ball growth
        ball_radius += BALL_GROWTH_RATE

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the liquid effect
        anim += 0.02
        int_ball_radius = int(ball_radius)  # Convert ball_radius to an integer for range
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
        draw_ball_and_lasers(screen, ball_x, ball_y, int(ball_radius), current_lasers)
    else:
        # Clear the screen and show text
        screen.fill(BACKGROUND_COLOR)
        text_surface = font.render('AI Will Take Your Job!', True, FRAME_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Draw the RESTART button
        draw_button(screen, "RESTART", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 40, 100, 40, FRAME_COLOR, FRAME_COLOR)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()