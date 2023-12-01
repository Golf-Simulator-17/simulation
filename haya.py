import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.animation import FuncAnimation
import asyncio
import threading

def update_position_velocity(initial_velocity, acceleration, time):
    vx0, vy0, vz0 = initial_velocity
    ax, ay, az = acceleration

    # Update velocity
    vx = vx0 + ax * time
    vy = vy0 + ay * time
    vz = vz0 + az * time

    # Update position
    x = vx0 * time + 0.5 * ax * time**2
    y = vy0 * time + 0.5 * ay * time**2
    z = vz0 * time + 0.5 * az * time**2

    return (x, y, z), (vx, vy, vz)

# Read values from the CSV file


def analysis():
    accelerometer_data = []
    gyroscope_data = []
    # file_path = "/home/samantha/college/ece477/golf_application/hit_info/receivedData20231129_210425.csv"
    file_path = "hitinfo.csv"
    with open(file_path, newline='') as csvfile:
        data_reader = csv.reader(csvfile)
        temp_data = []
        row_count = 1
        for row in data_reader:
            temp_data.append(float(row[0]))
            if len(temp_data) == 3 and row_count < 60:
                accelerometer_data.append(temp_data)
                temp_data = []
            elif len(temp_data) == 3 and row_count >= 60:
                gyroscope_data.append(temp_data)
                temp_data = []
            row_count += 1

    accelerometer_data = np.array(accelerometer_data)
    print(accelerometer_data)
    gyroscope_data = np.array(gyroscope_data)
    print(gyroscope_data)
    time_interval = 0.00015  # in seconds
    time_array = np.arange(0, len(accelerometer_data) * time_interval, time_interval)
    print(time_array)
    # Calculate velocity
    velocity_data = velocity(accelerometer_data, time_array)    
    print("MAX VELOCITY: " + str(accelerometer_data))
    
    #Calculate Position 
    position_data = position(velocity_data, time_array)

    # Hardcoded initial velocity and acceleration values
    initial_velocity = (max(abs(accelerometer_data[:][1]))*0.3, max(abs(accelerometer_data[:][1]))*0.3, max(abs(accelerometer_data[:][1]))*0.3)
    print("INITAL VELO:" + str(initial_velocity))
    acceleration = (-0.26*9.6, -9.8, -0.26*9.8)

# Time for which you want to update the position and velocity
    time = 5

# Update the position and velocity based on the given time
    final_position, final_velocity = update_position_velocity(initial_velocity, acceleration, time)

# Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory
    ax.plot([0, final_position[0]], [0, final_position[1]], [0, final_position[2]], marker='o')

# Set axis labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

# Set plot title
    ax.set_title('Object Trajectory')

# Show the plot
    plt.show()

# Print the final position and velocity
    # print(f"Final Position: {final_position}")
    # print(f"Final Velocity: {final_velocity}")

def position(velocity, time):
    position = np.zeros_like(velocity)
    for i in range(1, len(time)):
        for j in range(3):  # 0:x, 1:y, 2:z
            position[i, j] = simpson(velocity[:i, j], time[:i])
    return position

def velocity(acceleration, time):
    velocity = np.zeros_like(acceleration)
    for i in range(1, len(time)):
        for j in range(3):  # 0:x, 1:y, 2:z
            velocity[i, j] = simpson(acceleration[:i, j], time[:i])
    return velocity

analysis()