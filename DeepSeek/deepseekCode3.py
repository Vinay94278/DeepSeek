# Prompt :- Create a visually stunning fireworks simulation where particles shoot up from the ground, explode into vibrant, colorful patterns, and fade out naturally. The simulation should include realistic physics with gravity affecting the particles, slight randomness in explosion patterns, and smooth color transitions. Implement multiple firework launches at random intervals, each with different colors and explosion styles (e.g., circular, starburst, and cascading effects). The particles should have a fading effect to simulate realistic fireworks. Use Python with Pygame or Matplotlib to animate the scene in real-time.

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Simulation")

# Colors
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Gravity constant
GRAVITY = 0.1

# Particle class
class Particle:
    def __init__(self, x, y, color, speed, angle):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.angle = angle
        self.age = 0
        self.lifetime = random.randint(50, 100)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed + GRAVITY
        self.speed *= 0.95  # Air resistance
        self.age += 1

    def is_alive(self):
        return self.age < self.lifetime

# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = random.choice(COLORS)
        self.particles = []
        self.exploded = False

    def launch(self):
        self.y -= 5  # Move upwards

        if random.random() < 0.02:  # Random chance to explode
            self.explode()

    def explode(self):
        self.exploded = True
        num_particles = random.randint(50, 100)
        for _ in range(num_particles):
            speed = random.uniform(2, 5)
            angle = random.uniform(0, 2 * math.pi)
            self.particles.append(Particle(self.x, self.y, self.color, speed, angle))

    def update(self):
        if not self.exploded:
            self.launch()
        else:
            for particle in self.particles:
                particle.move()
            self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
        else:
            for particle in self.particles:
                alpha = 255 * (1 - particle.age / particle.lifetime)
                color = (*particle.color, alpha)
                pygame.draw.circle(screen, color, (int(particle.x), int(particle.y)), 2)

# Main loop
clock = pygame.time.Clock()
fireworks = []

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Launch new fireworks at random intervals
    if random.random() < 0.05:
        fireworks.append(Firework())

    # Update and draw fireworks
    for firework in fireworks:
        firework.update()
        firework.draw()

    # Remove dead fireworks
    fireworks = [f for f in fireworks if not f.exploded or len(f.particles) > 0]

    pygame.display.flip()
    clock.tick(30)

pygame.quit()