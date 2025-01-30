# Prompt :- Simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions. Use Python to create a real-time visualization of the system's evolution.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import simpledialog

# Constants
g = 9.81  # Gravity (m/s^2)
L1, L2 = 1.0, 1.0  # Lengths of the rods (m)
m1, m2 = 1.0, 1.0  # Masses (kg)

def equations(t, y):
    """Defines the system of equations for the double pendulum."""
    theta1, z1, theta2, z2 = y
    
    delta = theta2 - theta1
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
    den2 = (L2 / L1) * den1
    
    dtheta1_dt = z1
    dtheta2_dt = z2
    dz1_dt = (m2 * L1 * z1 ** 2 * np.sin(delta) * np.cos(delta) +
              m2 * g * np.sin(theta2) * np.cos(delta) +
              m2 * L2 * z2 ** 2 * np.sin(delta) -
              (m1 + m2) * g * np.sin(theta1)) / den1
    dz2_dt = (-L1 * z1 ** 2 * np.sin(delta) * np.cos(delta) +
              g * np.sin(theta1) * np.cos(delta) -
              L2 * z2 ** 2 * np.sin(delta) * (m1 + m2) / m2 -
              g * np.sin(theta2)) / den2
    
    return [dtheta1_dt, dz1_dt, dtheta2_dt, dz2_dt]

# Initial conditions (theta1, omega1, theta2, omega2 in radians)
def get_initial_conditions():
    root = tk.Tk()
    root.withdraw()
    theta1 = np.radians(float(simpledialog.askstring("Input", "Enter initial theta1 (degrees):")))
    theta2 = np.radians(float(simpledialog.askstring("Input", "Enter initial theta2 (degrees):")))
    return [theta1, 0, theta2, 0]

# Time array
t_span = (0, 20)  # Simulate for 20 seconds
t_eval = np.linspace(0, 20, 1000)

# Get user input
initial_conditions = get_initial_conditions()

# Solve the differential equations
sol = solve_ivp(equations, t_span, initial_conditions, t_eval=t_eval, method='RK45')

# Extract angles
theta1, theta2 = sol.y[0], sol.y[2]

# Convert to Cartesian coordinates
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

# Create animation
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
trace_x, trace_y = [], []
trace, = ax.plot([], [], 'r-', alpha=0.5)

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(frame):
    trace_x.append(x2[frame])
    trace_y.append(y2[frame])
    
    line.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
    trace.set_data(trace_x, trace_y)
    return line, trace

ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=20)
plt.show()
