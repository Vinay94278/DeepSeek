# Prompt :- Simulate multiple balls bouncing off the walls and colliding with each other, following gravity and momentum conservation.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
NUM_BALLS = 5
RADIUS = 0.1
WIDTH, HEIGHT = 10, 10
GRAVITY = 9.81
DT = 0.01

# Ball class
class Ball:
    def __init__(self, position, velocity, mass):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass

    def update_position(self):
        self.position += self.velocity * DT
        self.velocity[1] -= GRAVITY * DT  # Apply gravity

    def check_wall_collision(self):
        if self.position[0] <= RADIUS or self.position[0] >= WIDTH - RADIUS:
            self.velocity[0] *= -1  # Reverse horizontal velocity
        if self.position[1] <= RADIUS or self.position[1] >= HEIGHT - RADIUS:
            self.velocity[1] *= -1  # Reverse vertical velocity

    def check_ball_collision(self, other):
        distance = np.linalg.norm(self.position - other.position)
        if distance <= 2 * RADIUS:
            # Elastic collision calculation
            normal = (other.position - self.position) / distance
            tangent = np.array([-normal[1], normal[0]])
            v1n = np.dot(self.velocity, normal)
            v1t = np.dot(self.velocity, tangent)
            v2n = np.dot(other.velocity, normal)
            v2t = np.dot(other.velocity, tangent)

            # Conservation of momentum and kinetic energy
            v1n_new = (v1n * (self.mass - other.mass) + 2 * other.mass * v2n) / (self.mass + other.mass)
            v2n_new = (v2n * (other.mass - self.mass) + 2 * self.mass * v1n) / (self.mass + other.mass)

            # Update velocities
            self.velocity = v1n_new * normal + v1t * tangent
            other.velocity = v2n_new * normal + v2t * tangent

# Initialize balls
balls = [Ball(
    position=[np.random.uniform(RADIUS, WIDTH - RADIUS), np.random.uniform(RADIUS, HEIGHT - RADIUS)],
    velocity=[np.random.uniform(-5, 5), np.random.uniform(-5, 5)],
    mass=np.random.uniform(0.5, 1.5)
) for _ in range(NUM_BALLS)]

# Animation setup
fig, ax = plt.subplots()
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
circles = [plt.Circle((ball.position[0], ball.position[1]), RADIUS, color='b') for ball in balls]
for circle in circles:
    ax.add_patch(circle)

def update(frame):
    for i, ball in enumerate(balls):
        ball.update_position()
        ball.check_wall_collision()
        for other in balls[i+1:]:
            ball.check_ball_collision(other)
        circles[i].center = (ball.position[0], ball.position[1])
    return circles

ani = FuncAnimation(fig, update, frames=200, interval=DT*1000, blit=True)
plt.show()