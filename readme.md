# Prompt
Simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions. Use Python to create a real-time visualization of the system's evolution.

# Output Provided By Deepseek
To simulate a double pendulum system with chaotic motion and allow user interaction to change initial conditions, we can use Python with libraries such as numpy for numerical computations and matplotlib for real-time visualization. Below is a step-by-step guide and code to achieve this:

Step 1: Set Up the Environment
Make sure you have the necessary libraries installed:

```bash
pip install numpy matplotlib
```

Step 2: Define the Double Pendulum System
The double pendulum system can be described by a set of differential equations. We will use the Euler method for simplicity, though more advanced methods like Runge-Kutta could be used for better accuracy.

Step 3: Create the Simulation and Visualization
We will use matplotlib to create an interactive plot where the user can change the initial conditions.

Here is the complete Python code:

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
g = 9.81  # gravity (m/s^2)
L1 = 1.0  # length of the first pendulum (m)
L2 = 1.0  # length of the second pendulum (m)
m1 = 1.0  # mass of the first pendulum (kg)
m2 = 1.0  # mass of the second pendulum (kg)

# Initial conditions
theta1 = np.pi / 2  # initial angle of the first pendulum (rad)
theta2 = np.pi / 2  # initial angle of the second pendulum (rad)
omega1 = 0.0  # initial angular velocity of the first pendulum (rad/s)
omega2 = 0.0  # initial angular velocity of the second pendulum (rad/s)

# Time step and simulation time
dt = 0.01
t_max = 30.0
t = np.arange(0, t_max, dt)

# Function to compute derivatives
def derivatives(state, t):
    theta1, omega1, theta2, omega2 = state
    dtheta1 = omega1
    dtheta2 = omega2

    delta_theta = theta2 - theta1
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta_theta) ** 2
    den2 = (L2 / L1) * den1

    domega1 = ((m2 * L2 * omega2 ** 2 * np.sin(delta_theta) -
                m2 * g * np.sin(theta2) * np.cos(delta_theta) +
                (m1 + m2) * g * np.sin(theta1)) / den1)
    
    domega2 = ((-L1 / L2) * (omega1 ** 2 * np.sin(delta_theta) +
                             g * np.sin(theta2) -
                             g * np.sin(theta1) * np.cos(delta_theta)) / den2)

    return [dtheta1, domega1, dtheta2, domega2]

# Function to update the plot
def update(val):
    global theta1, theta2, omega1, omega2
    theta1 = slider_theta1.val
    theta2 = slider_theta2.val
    omega1 = slider_omega1.val
    omega2 = slider_omega2.val
    state = [theta1, omega1, theta2, omega2]
    for i in range(len(t)):
        state = state + np.array(derivatives(state, t[i])) * dt
        x1 = L1 * np.sin(state[0])
        y1 = -L1 * np.cos(state[0])
        x2 = x1 + L2 * np.sin(state[2])
        y2 = y1 - L2 * np.cos(state[2])
        line.set_data([0, x1, x2], [0, y1, y2])
        fig.canvas.draw_idle()

# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
line, = ax.plot([], [], 'o-', lw=2)

# Create sliders for initial conditions
axcolor = 'lightgoldenrodyellow'
ax_theta1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_theta2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_omega1 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_omega2 = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)

slider_theta1 = Slider(ax_theta1, 'Theta1', 0, 2 * np.pi, valinit=theta1)
slider_theta2 = Slider(ax_theta2, 'Theta2', 0, 2 * np.pi, valinit=theta2)
slider_omega1 = Slider(ax_omega1, 'Omega1', -10, 10, valinit=omega1)
slider_omega2 = Slider(ax_omega2, 'Omega2', -10, 10, valinit=omega2)

# Update the plot when sliders are changed
slider_theta1.on_changed(update)
slider_theta2.on_changed(update)
slider_omega1.on_changed(update)
slider_omega2.on_changed(update)

# Initial plot
update(0)

plt.show()
```

Explanation:
Constants and Initial Conditions: We define the physical constants and initial conditions for the double pendulum.

Derivatives Function: This function computes the derivatives of the angles and angular velocities using the equations of motion for the double pendulum.

Update Function: This function updates the plot based on the current state of the system and the slider values.

Sliders: We create sliders to allow the user to interactively change the initial conditions.

Real-time Visualization: The plot is updated in real-time as the user changes the sliders.

Running the Code:
When you run the code, a window will open showing the double pendulum simulation. You can use the sliders to change the initial angles and angular velocities, and observe how the system evolves over time.

This simulation demonstrates the chaotic behavior of the double pendulum, where small changes in initial conditions can lead to vastly different outcomes.