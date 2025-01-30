# Prompt :- Simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions. Use Python to create a real-time visualization of the system's evolution.

import pygame
import numpy as np
from numpy import sin, cos
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
G = 9.81  # gravitational constant
L1 = 100  # length of first pendulum
L2 = 100  # length of second pendulum
M1 = 1.0  # mass of first pendulum
M2 = 1.0  # mass of second pendulum

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class DoublePendulum:
    def __init__(self, theta1, theta2, p1, p2):
        self.theta1 = theta1
        self.theta2 = theta2
        self.p1 = p1  # angular momentum of pendulum 1
        self.p2 = p2  # angular momentum of pendulum 2
        self.trail = []
        
    def derivatives(self):
        dtheta1 = 6.0/(M1+M2)/(L1**2) * self.p1 - 3.0*cos(self.theta1-self.theta2)/(M1+M2)/(L1**2) * self.p2
        dtheta2 = 3.0*cos(self.theta1-self.theta2)/(M1+M2)/(L1**2) * self.p1 + 3.0/(M1+M2)/(L1**2) * self.p2
        
        dp1 = -(M1+M2)*G*L1*sin(self.theta1) - 3.0*sin(self.theta1-self.theta2)*dtheta2**2
        dp2 = -M2*G*L2*sin(self.theta2) + 3.0*sin(self.theta1-self.theta2)*dtheta1**2
        
        return dtheta1, dtheta2, dp1, dp2
    
    def update(self, dt):
        dtheta1, dtheta2, dp1, dp2 = self.derivatives()
        
        self.theta1 += dtheta1 * dt
        self.theta2 += dtheta2 * dt
        self.p1 += dp1 * dt
        self.p2 += dp2 * dt
        
        # Calculate positions
        x1 = L1 * sin(self.theta1)
        y1 = L1 * cos(self.theta1)
        x2 = x1 + L2 * sin(self.theta2)
        y2 = y1 + L2 * cos(self.theta2)
        
        # Add to trail
        self.trail.append((int(x2 + WIDTH//2), int(y2 + HEIGHT//2)))
        if len(self.trail) > 100:  # Keep only last 100 points
            self.trail.pop(0)
            
        return (x1, y1), (x2, y2)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum Simulation")
clock = pygame.time.Clock()

# Initial conditions
pendulum = DoublePendulum(np.pi/2, np.pi/2, 0, 0)
paused = False
dt = 1/FPS

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:  # Reset
                pendulum = DoublePendulum(np.pi/2, np.pi/2, 0, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Change initial conditions based on mouse position
            x, y = pygame.mouse.get_pos()
            pendulum.theta1 = np.arctan2(x - WIDTH//2, y - HEIGHT//2)
            pendulum.p1 = 0
            pendulum.p2 = 0
            pendulum.trail = []

    if not paused:
        # Update physics
        pos1, pos2 = pendulum.update(dt)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw trail
        if len(pendulum.trail) > 1:
            pygame.draw.lines(screen, BLUE, False, pendulum.trail, 1)
        
        # Draw pendulum
        center = (WIDTH//2, HEIGHT//2)
        p1 = (int(pos1[0] + WIDTH//2), int(pos1[1] + HEIGHT//2))
        p2 = (int(pos2[0] + WIDTH//2), int(pos2[1] + HEIGHT//2))
        
        pygame.draw.line(screen, WHITE, center, p1, 2)
        pygame.draw.line(screen, WHITE, p1, p2, 2)
        pygame.draw.circle(screen, RED, p1, 10)
        pygame.draw.circle(screen, RED, p2, 10)
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        text = font.render("Space: Pause/Resume | R: Reset | Click: Change Initial Position", True, WHITE)
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()