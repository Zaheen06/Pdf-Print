import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [2, -5]
gravity = 0.5
friction = 0.99

# Hexagon properties
hexagon_radius = 200
hexagon_angle = 0
hexagon_speed = 0.01

# Function to draw hexagon
def draw_hexagon(surface, color, center, radius, angle):
    points = []
    for i in range(6):
        theta = math.radians(60 * i) + angle
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, 2)
    return points

# Function to check collision with hexagon walls
def check_collision(ball_pos, ball_vel, hexagon_points):
    for i in range(6):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % 6]
        wall_vector = (p2[0] - p1[0], p2[1] - p1[1])
        wall_length = math.hypot(wall_vector[0], wall_vector[1])
        wall_normal = (wall_vector[1] / wall_length, -wall_vector[0] / wall_length)
        
        ball_to_wall = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        distance = ball_to_wall[0] * wall_normal[0] + ball_to_wall[1] * wall_normal[1]
        
        if abs(distance) < ball_radius:
            ball_pos[0] -= distance * wall_normal[0]
            ball_pos[1] -= distance * wall_normal[1]
            ball_vel[0] -= 2 * distance * wall_normal[0]
            ball_vel[1] -= 2 * distance * wall_normal[1]
            return

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_vel[0] *= friction
    ball_vel[1] *= friction

    # Update hexagon rotation
    hexagon_angle += hexagon_speed

    # Draw everything
    screen.fill(BLACK)
    hexagon_points = draw_hexagon(screen, WHITE, (WIDTH // 2, HEIGHT // 2), hexagon_radius, hexagon_angle)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Check for collision
    check_collision(ball_pos, ball_vel, hexagon_points)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()