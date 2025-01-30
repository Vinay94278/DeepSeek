# Prompt :- Simulate multiple balls bouncing off the walls and colliding with each other, following gravity and momentum conservation.

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
ELASTICITY = 0.95  # Energy conservation coefficient
BALL_COUNT = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.mass = radius * radius  # Mass proportional to area
        self.color = random.choice(COLORS)

    def move(self):
        # Apply gravity
        self.dy += GRAVITY
        
        # Update position
        self.x += self.dx
        self.y += self.dy

        # Wall collisions
        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx *= -ELASTICITY
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.dx *= -ELASTICITY

        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy *= -ELASTICITY
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy *= -ELASTICITY

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def check_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx * dx + dy * dy)
    
    if distance < ball1.radius + ball2.radius:
        # Collision detected - calculate collision response
        # Normal vector
        nx = dx / distance
        ny = dy / distance
        
        # Relative velocity
        dvx = ball2.dx - ball1.dx
        dvy = ball2.dy - ball1.dy
        
        # Normal velocity
        normal_vel = dvx * nx + dvy * ny
        
        # Only proceed if objects are moving toward each other
        if normal_vel < 0:
            # Impact speed
            imp = -(1 + ELASTICITY) * normal_vel
            
            # Total mass
            total_mass = ball1.mass + ball2.mass
            
            # Impulse
            imp1 = (2 * ball2.mass * imp) / total_mass
            imp2 = (2 * ball1.mass * imp) / total_mass
            
            # Update velocities
            ball1.dx -= imp1 * nx
            ball1.dy -= imp1 * ny
            ball2.dx += imp2 * nx
            ball2.dy += imp2 * ny

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Balls Physics Simulation")
    clock = pygame.time.Clock()

    # Create balls with random positions and sizes
    balls = []
    for _ in range(BALL_COUNT):
        radius = random.randint(20, 40)
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)
        balls.append(Ball(x, y, radius))

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ball positions
        for ball in balls:
            ball.move()

        # Check for collisions between all pairs of balls
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                check_collision(balls[i], balls[j])

        # Draw
        screen.fill(BLACK)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()