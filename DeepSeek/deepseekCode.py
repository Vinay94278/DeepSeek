# Prompt :- Simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions. Use Python to create a real-time visualization of the system's evolution.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp

def double_pendulum(t, y, L1, L2, m1, m2, g):
    theta1, z1, theta2, z2 = y
    
    delta = theta2 - theta1
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) * np.cos(delta)
    den2 = (L2 / L1) * den1
    
    dtheta1 = z1
    dz1 = (m2 * L1 * z1 * z1 * np.sin(delta) * np.cos(delta)
           + m2 * g * np.sin(theta2) * np.cos(delta)
           + m2 * L2 * z2 * z2 * np.sin(delta)
           - (m1 + m2) * g * np.sin(theta1)) / den1
    
    dtheta2 = z2
    dz2 = (-m2 * L2 * z2 * z2 * np.sin(delta) * np.cos(delta)
           + (m1 + m2) * g * np.sin(theta1) * np.cos(delta)
           - (m1 + m2) * L1 * z1 * z1 * np.sin(delta)
           - (m1 + m2) * g * np.sin(theta2)) / den2
    
    return [dtheta1, dz1, dtheta2, dz2]

# Parameters
L1 = 1.0
L2 = 1.0
m1 = 1.0
m2 = 1.0
g = 9.81

# Initial conditions
theta1_0 = np.pi / 2
theta2_0 = np.pi / 2
z1_0 = 0.0
z2_0 = 0.0

y0 = [theta1_0, z1_0, theta2_0, z2_0]

# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# Initialize the pendulum lines
line, = ax.plot([], [], 'o-', lw=2)

# Function to update the pendulum position
def update_pendulum(theta1, theta2):
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    line.set_data([0, x1, x2], [0, y1, y2])
    return line,

# Function to solve the ODE and update the plot
def animate(t):
    sol = solve_ivp(double_pendulum, [0, t], y0, args=(L1, L2, m1, m2, g), t_eval=[t])
    theta1, theta2 = sol.y[0, -1], sol.y[2, -1]
    update_pendulum(theta1, theta2)
    return line,

# Animation function
def run_animation():
    from matplotlib.animation import FuncAnimation
    ani = FuncAnimation(fig, animate, frames=np.linspace(0, 10, 300), interval=50, blit=True)
    plt.show()

# Create sliders for initial conditions
axcolor = 'lightgoldenrodyellow'
ax_theta1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_theta2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

theta1_slider = Slider(ax_theta1, 'Theta1', 0.0, 2 * np.pi, valinit=theta1_0)
theta2_slider = Slider(ax_theta2, 'Theta2', 0.0, 2 * np.pi, valinit=theta2_0)

# Update function for sliders
def update(val):
    global y0
    y0[0] = theta1_slider.val
    y0[2] = theta2_slider.val

theta1_slider.on_changed(update)
theta2_slider.on_changed(update)

# Run the animation
run_animation()