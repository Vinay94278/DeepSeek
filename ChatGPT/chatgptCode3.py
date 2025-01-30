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
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 20, 147)]

# Gravity
GRAVITY = 0.05

class Particle:
    def __init__(self, x, y, color, angle, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.alpha = 255  # Initial opacity

    def update(self):
        # Move particle based on angle and speed
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.speed *= 0.98  # Slow down over time
        self.y += GRAVITY  # Apply gravity
        self.alpha = max(0, self.alpha - 4)  # Fade out
        self.lifetime -= 1

    def draw(self, surface):
        if self.alpha > 0:
            color = (*self.color, self.alpha)  # Apply alpha for fading
            s = pygame.Surface((5, 5), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (2, 2), 2)
            surface.blit(s, (int(self.x), int(self.y)))

class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = random.choice(COLORS)
        self.speed = random.uniform(5, 7)
        self.exploded = False
        self.explosion_particles = []

    def update(self):
        if not self.exploded:
            self.y -= self.speed  # Move up
            self.speed *= 0.98  # Slow down
            if self.speed < 1:  # Explosion trigger
                self.explode()
        else:
            for particle in self.explosion_particles:
                particle.update()
            self.explosion_particles = [p for p in self.explosion_particles if p.lifetime > 0]

    def explode(self):
        self.exploded = True
        num_particles = random.randint(30, 60)
        explosion_type = random.choice(["circle", "star", "cascade"])
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            lifetime = random.randint(40, 80)
            if explosion_type == "star" and _ % 2 == 0:
                angle += math.pi / 8  # Slight angle shift
            elif explosion_type == "cascade":
                speed *= random.uniform(0.5, 1.5)  # Varying speeds
            self.explosion_particles.append(Particle(self.x, self.y, self.color, angle, speed, lifetime))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
        else:
            for particle in self.explosion_particles:
                particle.draw(surface)

# Main loop
running = True
clock = pygame.time.Clock()
fireworks = []

while running:
    screen.fill(BLACK)
    
    if random.random() < 0.02:  # Random firework launch interval
        fireworks.append(Firework())
    
    for firework in fireworks:
        firework.update()
        firework.draw(screen)
    
    fireworks = [fw for fw in fireworks if not fw.exploded or fw.explosion_particles]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
