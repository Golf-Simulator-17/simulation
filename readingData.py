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

from golf_app import *

def analysis():
    accelerometer_data = []
    gyroscope_data = []
    file_path = "hitinfo.csv"
    with open(file_path, newline='') as csvfile:
        data_reader = csv.reader(csvfile)
        temp_data = []
        row_count = 1
        for row in data_reader:
            temp_data.append(float(row[0]))
            if len(temp_data) == 3 and row_count < 30:
                accelerometer_data.append(temp_data)
                temp_data = []
            elif len(temp_data) == 3 and row_count >= 30:
                gyroscope_data.append(temp_data)
                temp_data = []
            row_count += 1

    accelerometer_data = np.array(accelerometer_data)
    gyroscope_data = np.array(gyroscope_data)
    time_interval = 0.1  # in seconds
    time_array = np.arange(0, len(accelerometer_data) * time_interval, time_interval)

    # Calculate velocity
    velocity_data = velocity(accelerometer_data, time_array)    
    #graphVelocity(velocity_data)
    
    #Calculate Position 
    position_data = position(velocity_data, time_array)
    #graphPosition(position_data)
    # # Sample data for velocity
    # time = np.linspace(0, 5, num=100)  # Time from 0 to 5 seconds
    # initial_velocity = np.array([10, 15, 25])  # Initial velocity vector
    # gravity = np.array([0, 0, -9.81])  # Gravity vector

    # # Calculate velocity at each point in time (v = u + at)
    # velocity_data = np.array([initial_velocity + gravity * t for t in time])

    # # Sample data for position (s = ut + 0.5at^2)
    # position_data = np.array([initial_velocity * t + 0.5 * gravity * t**2 for t in time])

    # # Transpose the data for plotting
    # velocity_data = velocity_data.T
    # position_data = position_data.T

    display_graphs(velocity_data, position_data)
    # Display the results
    print("Accelerometer Data:", accelerometer_data)
    # print("Gyroscope Data:", gyroscope_data)
    print("Velocity Data:", velocity_data)
    #print("Position Data:", position_data)

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

def update_graph(num, data, line):
    # Make sure we only use the data up to the current frame
    line.set_data(data[:2, :num+1])
    line.set_3d_properties(data[2, :num+1])
    return line,

def animate_graph(fig, data, ax):
    # Setting the axes properties
    # ax.set_xlim([np.min(data[0,:]), np.max(data[0,:])])
    # ax.set_ylim([np.min(data[1,:]), np.max(data[1,:])])
    # ax.set_zlim([np.min(data[2,:]), np.max(data[2,:])])

    # Creating a line that we will update
    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], color='blue')
    
    # Starting the animation
    ani = FuncAnimation(fig, update_graph, frames=len(data.T), fargs=(data, line), interval=100, blit=False)
    return ani

def display_graphs(velocity_data, position_data):
    # New window for graphs
    graph_window = tk.Toplevel()
    graph_window.title("Simulation Results")
    graph_window.geometry("1200x600")

    redo_button = tk.Button(graph_window, text="Redo Simulation", command=lambda: threading.Thread(target=redo).start())
    redo_button.pack()  # Adding padding for spacing



    # Create and place velocity graph
    fig_velocity = Figure(figsize=(6, 6))
    ax_velocity = fig_velocity.add_subplot(111, projection='3d')
    ax_velocity.set_xlabel('X Velocity')
    ax_velocity.set_ylabel('Y Velocity')
    ax_velocity.set_zlabel('Z Velocity')
    ax_velocity.set_title('3D Velocity Trajectory')
    canvas_velocity = FigureCanvasTkAgg(fig_velocity, master=graph_window)
    canvas_velocity.draw()
    canvas_velocity.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create and place position graph
    fig_position = Figure(figsize=(6, 6))
    ax_position = fig_position.add_subplot(111, projection='3d')
    ax_position.set_xlabel('X Position')
    ax_position.set_ylabel('Y Position')
    ax_position.set_zlabel('Z Position')
    ax_position.set_title('3D Position Trajectory')
    canvas_position = FigureCanvasTkAgg(fig_position, master=graph_window)
    canvas_position.draw()
    canvas_position.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    #adding graph window to actualyl show the lines moving
    graph_window.velocity_ani = animate_graph(fig_velocity, velocity_data, ax_velocity)
    graph_window.position_ani = animate_graph(fig_position, position_data, ax_position)

def redo():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    loop.close()
def start_simulation():
    bitch()
    analysis()
    pass

def stop_simulation():
    # need to create stop code
    pass

def run_gui():
    root = tk.Tk()
    root.title("Golf Simulator")
    root.geometry("800x600")

    # Load and set the background image
    background_image = Image.open("golf_course.webp")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    filename = "hit_info/receivedData20231130_162331.csv"
    # Welcome Message
    welcome_label = tk.Label(root, text="Welcome to the Golf Simulator", font=("Arial", 24), bg="white")
    welcome_label.pack(pady=20)

    # Start and Stop Simulation buttons
    start_button = ttk.Button(root, text="Start Simulation", command=lambda: start_simulation())
    start_button.pack(pady=10)  # Adding padding for spacing

    # stop_button = ttk.Button(root, text="Stop Simulation", command=stop_simulation)
    # stop_button.pack(pady=10)  # Adding padding for spacing

    root.mainloop()
if __name__ == "__main__":

    run_gui()
    
