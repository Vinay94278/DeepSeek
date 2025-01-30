# Prompt :- Simulate multiple balls bouncing off the walls and colliding with each other, following gravity and momentum conservation.

import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
BALL_COUNT = 10
GRAVITY = 0.2
FRICTION = 0.99

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
    
    def move(self):
        self.vy += GRAVITY  # Apply gravity
        self.x += self.vx
        self.y += self.vy
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Collision with walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Collision detection and response

def resolve_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < ball1.radius + ball2.radius:
        angle = math.atan2(dy, dx)
        
        # Decompose velocities into parallel and perpendicular components
        v1_parallel = ball1.vx * math.cos(angle) + ball1.vy * math.sin(angle)
        v2_parallel = ball2.vx * math.cos(angle) + ball2.vy * math.sin(angle)
        
        # Elastic collision formula
        v1_new = ((ball1.mass - ball2.mass) * v1_parallel + 2 * ball2.mass * v2_parallel) / (ball1.mass + ball2.mass)
        v2_new = ((ball2.mass - ball1.mass) * v2_parallel + 2 * ball1.mass * v1_parallel) / (ball1.mass + ball2.mass)
        
        # Convert back to x, y components
        ball1.vx += (v1_new - v1_parallel) * math.cos(angle)
        ball1.vy += (v1_new - v1_parallel) * math.sin(angle)
        ball2.vx += (v2_new - v2_parallel) * math.cos(angle)
        ball2.vy += (v2_new - v2_parallel) * math.sin(angle)
        
        # Separate the balls to avoid overlap
        overlap = ball1.radius + ball2.radius - distance
        ball1.x -= math.cos(angle) * overlap / 2
        ball1.y -= math.sin(angle) * overlap / 2
        ball2.x += math.cos(angle) * overlap / 2
        ball2.y += math.sin(angle) * overlap / 2

# Create balls
balls = [
    Ball(
        random.randint(50, WIDTH - 50),
        random.randint(50, HEIGHT - 50),
        random.randint(10, 20),
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        random.uniform(1, 3)
    )
    for _ in range(BALL_COUNT)
]

running = True
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for i, ball in enumerate(balls):
        ball.move()
        ball.draw()
        for j in range(i + 1, len(balls)):
            resolve_collision(ball, balls[j])
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()