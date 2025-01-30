# Prompt :- Create a visually stunning fireworks simulation where particles shoot up from the ground, explode into vibrant, colorful patterns, and fade out naturally. The simulation should include realistic physics with gravity affecting the particles, slight randomness in explosion patterns, and smooth color transitions. Implement multiple firework launches at random intervals, each with different colors and explosion styles (e.g., circular, starburst, and cascading effects). The particles should have a fading effect to simulate realistic fireworks. Use Python with Pygame or Matplotlib to animate the scene in real-time.

import pygame
import random
import math
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Particle:
    def __init__(self, x, y, color, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.color = list(color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.alpha = 255
        self.lifetime = random.randint(30, 60)
        self.age = 0
        
    def update(self):
        # Apply gravity
        self.velocity_y += 0.15
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Age the particle
        self.age += 1
        self.alpha = int(255 * (1 - self.age / self.lifetime))
        
        # Fade out color
        self.color[3] = self.alpha
        
    def is_alive(self):
        return self.age < self.lifetime

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exploded = False
        self.particles = []
        self.velocity_y = random.uniform(-16, -12)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
            255
        )
        
    def explode(self):
        num_particles = random.randint(50, 80)
        explosion_type = random.choice(['circular', 'starburst', 'cascade'])
        
        if explosion_type == 'circular':
            for i in range(num_particles):
                angle = (i / num_particles) * 2 * math.pi
                speed = random.uniform(3, 6)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append(Particle(self.x, self.y, self.color, vx, vy))
                
        elif explosion_type == 'starburst':
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 8)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append(Particle(self.x, self.y, self.color, vx, vy))
                
        else:  # cascade
            for _ in range(num_particles):
                vx = random.uniform(-3, 3)
                vy = random.uniform(-2, 4)
                self.particles.append(Particle(self.x, self.y, self.color, vx, vy))
    
    def update(self):
        if not self.exploded:
            self.velocity_y += 0.2
            self.y += self.velocity_y
            
            if self.velocity_y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.update()
            self.particles = [p for p in self.particles if p.is_alive()]
    
    def is_alive(self):
        return not self.exploded or len(self.particles) > 0

def main():
    clock = pygame.time.Clock()
    fireworks = []
    running = True
    last_launch = 0
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Launch firework at mouse click position
                x, _ = pygame.mouse.get_pos()
                fireworks.append(Firework(x, HEIGHT))
        
        # Automatic launching
        if current_time - last_launch > random.randint(500, 2000):
            x = random.randint(50, WIDTH - 50)
            fireworks.append(Firework(x, HEIGHT))
            last_launch = current_time
        
        # Update
        for firework in fireworks:
            firework.update()
        fireworks = [f for f in fireworks if f.is_alive()]
        
        # Draw
        screen.fill(BLACK)
        
        # Draw fireworks
        for firework in fireworks:
            if not firework.exploded:
                pygame.draw.circle(screen, firework.color, (int(firework.x), int(firework.y)), 2)
            
            for particle in firework.particles:
                color = list(particle.color)
                if len(color) == 4:  # Remove alpha if present
                    color = color[:3]
                surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*color, particle.alpha), (1, 1), 1)
                screen.blit(surface, (int(particle.x) - 1, int(particle.y) - 1))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()