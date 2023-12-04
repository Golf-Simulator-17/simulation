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
    print(velocity_data)
    #graphVelocity(velocity_data)
    
    #Calculate Position 
    position_data = position(velocity_data, time_array)
    # print(position_data)

    # fig,(axa,axv,axp,aya,ayv,ayp,aza,azv,azp) = plt.subplots(9)

    # axa.plot(time_array, accelerometer_data[:,0])
    # axa.set_xlabel("Time (ms)")
    # axa.set_ylabel("Acceleration (m^2/s)")
    # axa.set_title("Acceleration vs Time X-axis")

    # axv.plot(time_array, velocity_data[:,0])
    # axv.set_xlabel("Time (ms)")
    # axv.set_ylabel("Velocity (m/s)")
    # axv.set_title("Velocity vs Time X-axis")

    # axp.plot(time_array, position_data[:,0])
    # axp.set_xlabel("Time (ms)")
    # axp.set_ylabel("Position (m) X-Axis")
    # axp.set_title("Time vs Position X-axis")

    # aya.plot(time_array, accelerometer_data[:,1])
    # aya.set_xlabel("Time (ms)")
    # aya.set_ylabel("Acceleration (m^2/s)")
    # aya.set_title("Acceleration vs Time Y-axis")

    # ayv.plot(time_array, velocity_data[:,1])
    # ayv.set_xlabel("Time (ms)")
    # ayv.set_ylabel("Velocity (m/s)")
    # ayv.set_title("Velocity vs Time Y-axis")

    # ayp.plot(time_array, position_data[:,1])
    # ayp.set_xlabel("Time (ms)")
    # ayp.set_ylabel("Position (m) Y-Axis")
    # ayp.set_title("Time vs Position Y-axis")

    # aza.plot(time_array, accelerometer_data[:,2])
    # aza.set_xlabel("Time (ms)")
    # aza.set_ylabel("Acceleration (m^2/s)")
    # aza.set_title("Acceleration vs Time Z-axis")

    # azv.plot(time_array, velocity_data[:,2])
    # azv.set_xlabel("Time (ms)")
    # azv.set_ylabel("Velocity (m/s)")
    # azv.set_title("Velocity vs Time Z-axis")

    # azp.plot(time_array, position_data[:,2])
    # azp.set_xlabel("Time (ms)")
    # azp.set_ylabel("Position (m) Z-Axis")
    # azp.set_title("Time vs Position X-axis")

    # plt.show()

    # return

    display_graphs(velocity_data, position_data)
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

def display_graphs(velocity_data, position_data):
    # New window for graphs
    graph_window = tk.Toplevel()
    graph_window.title("Simulation Results")
    graph_window.geometry("1200x600")

    # Create and place velocity graph
    fig_velocity = Figure(figsize=(6, 6))
    ax_velocity = fig_velocity.add_subplot(111, projection='3d')
    ax_velocity.set_xlabel('X Velocity')
    ax_velocity.set_ylabel('Y Velocity')
    ax_velocity.set_zlabel('Z Velocity')
    ax_velocity.set_title('3D Velocity Trajectory')
    ax_velocity.plot(velocity_data[:, 0], velocity_data[:, 1], velocity_data[:, 2], marker='o')  # Plot velocity data
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
    ax_position.plot(position_data[:, 0], position_data[:, 1], position_data[:, 2], marker='o')  # Plot position data
    canvas_position = FigureCanvasTkAgg(fig_position, master=graph_window)
    canvas_position.draw()
    canvas_position.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
def redo(root):
    root.after(0, lambda: root.status_label.config(text="Not Ready . . ."))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(root))
    loop.close()
    root.after(0, analysis())

def start_simulation(root):
    run_bluetooth(root)
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
    start_button = ttk.Button(root, text="Start Simulation", command=lambda: start_simulation(root))
    start_button.pack(pady=10)  # Adding padding for spacing

    redo_button = ttk.Button(root, text="Redo Simulation", command=lambda: threading.Thread(target=redo(root)).start())
    redo_button.pack()  # Adding padding for spacing

    status_label = tk.Label(root, text="Status: Idle", font=("Arial", 14))
    status_label.pack(pady=10)
    root.status_label = status_label  # Make it accessible outside the function

    # stop_button = ttk.Button(root, text="Stop Simulation", command=stop_simulation)
    # stop_button.pack(pady=10)  # Adding padding for spacing

    root.mainloop()

if __name__ == "__main__":

    run_gui()
    # analysis()
    
