import csv
import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
def analysis():
    file_path = "received_data.csv"
    accelerometer_data = []
    gyroscope_data = []

    with open(file_path, newline='') as csvfile:
        data_reader = csv.reader(csvfile)
        temp_data = []
        for row in data_reader:
            temp_data.append(float(row[0]))
            if len(temp_data) == 6:
                accelerometer_data.append(temp_data[:3])
                gyroscope_data.append(temp_data[3:])
                temp_data = []

    accelerometer_data = np.array(accelerometer_data)
    gyroscope_data = np.array(gyroscope_data)
    time_interval = 0.1  # in seconds
    time_array = np.arange(0, len(accelerometer_data) * time_interval, time_interval)

    # Calculate velocity
    velocity_data = velocity(accelerometer_data, time_array)    
    graphVelocity(velocity_data)
    
    #Calculate Position 
    position_data = position(velocity_data, time_array)
    graphPosition(position_data)

    # Display the results
    print("Accelerometer Data:", accelerometer_data)
    print("Gyroscope Data:", gyroscope_data)
    print("Velocity Data:", velocity_data)
    print("Position Data:", position_data)


# Properly integrates each axis with the 2d arrays we have
def velocity(acceleration, time):
    velocity = np.zeros_like(acceleration)
    for i in range(1, len(time)):
        for j in range(3):  # 0:x, 1:y, 2:z
            velocity[i, j] = simpson(acceleration[:i, j], time[:i])
    return velocity

def position(velocity, time):
    position = np.zeros_like(velocity)
    for i in range(1, len(time)):
        for j in range(3):  # 0:x, 1:y, 2:z
            position[i, j] = simpson(velocity[:i, j], time[:i])
    return position

def graphVelocity(velocity_data):
    x_velocity = velocity_data[:, 0]
    y_velocity = velocity_data[:, 1]
    z_velocity = velocity_data[:, 2]

    # Creating a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the trajectory
    ax.plot(x_velocity, y_velocity, z_velocity)

    # Adding labels
    ax.set_xlabel('X Velocity')
    ax.set_ylabel('Y Velocity')
    ax.set_zlabel('Z Velocity')
    ax.set_title('3D Velocity Trajectory')

    # Display the plot
    plt.show()

def graphPosition(position_data):
    # Extracting x, y, z components of displacement
    x_position = position_data[:, 0]
    y_position = position_data[:, 1]
    z_position = position_data[:, 2]

    # Creating a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the trajectory
    ax.plot(x_position, y_position, z_position)

    # Adding labels and title
    ax.set_xlabel('X Displacement')
    ax.set_ylabel('Y Displacement')
    ax.set_zlabel('Z Displacement')
    ax.set_title('3D Displacement Trajectory')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    analysis()

