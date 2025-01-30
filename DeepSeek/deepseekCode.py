# Prompt :- Simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions. Use Python to create a real-time visualization of the system's evolution.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp

# Constants
g = 9.81  # gravity (m/s^2)
L1 = 1.0  # length of the first pendulum (m)
L2 = 1.0  # length of the second pendulum (m)
m1 = 1.0  # mass of the first pendulum (kg)
m2 = 1.0  # mass of the second pendulum (kg)

# Initial conditions
theta1_0 = np.pi / 2  # initial angle of the first pendulum (rad)
theta2_0 = np.pi / 2  # initial angle of the second pendulum (rad)
omega1_0 = 0.0  # initial angular velocity of the first pendulum (rad/s)
omega2_0 = 0.0  # initial angular velocity of the second pendulum (rad/s)

# Time parameters
t_max = 30  # maximum time (s)
dt = 0.05  # time step (s)
t_eval = np.arange(0, t_max, dt)

# Function to compute the derivatives of the state vector
def derivatives(t, y):
    theta1, theta2, omega1, omega2 = y
    
    # Equations of motion for a double pendulum
    delta_theta = theta2 - theta1
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta_theta) ** 2
    den2 = (L2 / L1) * den1
    
    dtheta1_dt = omega1
    dtheta2_dt = omega2
    
    domega1_dt = (m2 * L2 * omega2 ** 2 * np.sin(delta_theta) -
                  m2 * g * np.sin(theta2) * np.cos(delta_theta) +
                  (m1 + m2) * g * np.sin(theta1)) / den1
    
    domega2_dt = (-L1 / L2 * omega1 ** 2 * np.sin(delta_theta) -
                  g * np.sin(theta2) +
                  g * np.sin(theta1) * np.cos(delta_theta)) / den2
    
    return [dtheta1_dt, dtheta2_dt, domega1_dt, domega2_dt]

# Function to update the plot when sliders are changed
def update(val):
    # Get new initial conditions from sliders
    theta1_0 = slider_theta1.val
    theta2_0 = slider_theta2.val
    omega1_0 = slider_omega1.val
    omega2_0 = slider_omega2.val
    
    # Solve the ODE with new initial conditions
    sol = solve_ivp(derivatives, [0, t_max], [theta1_0, theta2_0, omega1_0, omega2_0], t_eval=t_eval)
    
    # Update the pendulum positions
    x1 = L1 * np.sin(sol.y[0])
    y1 = -L1 * np.cos(sol.y[0])
    x2 = x1 + L2 * np.sin(sol.y[1])
    y2 = y1 - L2 * np.cos(sol.y[1])
    
    # Update the plot
    line1.set_data([0, x1[-1]], [0, y1[-1]])
    line2.set_data([x1[-1], x2[-1]], [y1[-1], y2[-1]])
    trajectory.set_data(x2, y2)
    fig.canvas.draw_idle()

# Solve the initial ODE
sol = solve_ivp(derivatives, [0, t_max], [theta1_0, theta2_0, omega1_0, omega2_0], t_eval=t_eval)

# Extract the positions of the pendulums
x1 = L1 * np.sin(sol.y[0])
y1 = -L1 * np.cos(sol.y[0])
x2 = x1 + L2 * np.sin(sol.y[1])
y2 = y1 - L2 * np.cos(sol.y[1])

# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.grid()

# Plot the pendulum
line1, = ax.plot([0, x1[-1]], [0, y1[-1]], 'k-', lw=2)
line2, = ax.plot([x1[-1], x2[-1]], [y1[-1], y2[-1]], 'k-', lw=2)
trajectory, = ax.plot(x2, y2, 'r-', lw=1)

# Create sliders for initial conditions
axcolor = 'lightgoldenrodyellow'
ax_theta1 = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_theta2 = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_omega1 = plt.axes([0.2, 0.09, 0.65, 0.03], facecolor=axcolor)
ax_omega2 = plt.axes([0.2, 0.13, 0.65, 0.03], facecolor=axcolor)

slider_theta1 = Slider(ax_theta1, 'Theta1', 0, 2 * np.pi, valinit=theta1_0)
slider_theta2 = Slider(ax_theta2, 'Theta2', 0, 2 * np.pi, valinit=theta2_0)
slider_omega1 = Slider(ax_omega1, 'Omega1', -10, 10, valinit=omega1_0)
slider_omega2 = Slider(ax_omega2, 'Omega2', -10, 10, valinit=omega2_0)

# Attach the update function to the sliders
slider_theta1.on_changed(update)
slider_theta2.on_changed(update)
slider_omega1.on_changed(update)
slider_omega2.on_changed(update)

# Show the plot
plt.show()