import scipy

from matplotlib import pyplot as plt
import numpy as np
import datetime
# from mpl_toolkits.mplot3d import Axes3D
from scipy import integrate


def velocity(initial_velocity, acceleration, time):
    velocity = np.zeros(len(acceleration))
    for i in range(1, len(time)):
        velocity[i] = integrate.simpson(acceleration[0:i])
    return velocity

def position(initial_position, initial_velocity, velocity, time):
    position = np.zeros(len(time))
    for i in range(1, len(time)):
         position[i] = integrate.simpson(velocity[0:i])
    return position

def create_table(file_name):
    arr = np.loadtxt(file_name, delimiter=' ', dtype=str)
    header = arr[0]
    units = arr[1]
    arr = np.delete(arr, [0,1], 0)
    # arr = np.delete(arr, slice(5000,arr.shape[0]), 0)
    # arr = np.delete(arr, 0, 0)

    for i in range(len(arr)):
        # print(arr[i,0])
        arr[i,0] = int(datetime.datetime.strptime(arr[i][0] + " " + arr[i][1], '%Y/%m/%d %H:%M:%S.%f').strftime('%H%M%S%f'))
        # print(arr[i,0])
    
    arr = np.delete(arr, 1, axis=1)
    arr = np.delete(arr, arr.shape[1]-1, axis=1)
    header= np.delete(header, 1, axis=0)
    units = np.delete(units, 1, axis=0)
    
    arr= arr.astype(float)
    fig,(axa,axv,axp,aya,ayv,ayp,aza,azv,azp) = plt.subplots(9)

    axa.plot(arr[:,0], arr[:,1])
    axa.set_xlabel("Time (ms)")
    axa.set_ylabel("Acceleration (m^2/s)")
    axa.set_title("Acceleration vs Time X-axis")

    velocity_x = velocity(initial_velocity=0, acceleration=arr[:,1], time=arr[:,0])
    axv.plot(arr[:,0], velocity_x)
    axv.set_xlabel("Time (ms)")
    axv.set_ylabel("Velocity (m/s)")
    axv.set_title("Velocity vs Time X-axis")

    position_x = position(initial_position=0, initial_velocity=0, velocity=velocity_x, time=arr[:,0])
    axp.plot(arr[:,0], position_x)
    axp.set_xlabel("Time (ms)")
    axp.set_ylabel("Position (m) X-Axis")
    axv.set_title("Time vs Position X-axis")

    aya.plot(arr[:,0], arr[:,2])
    aya.set_xlabel("Time (ms)")
    aya.set_ylabel("Acceleration (m^2/s)")
    aya.set_title("Acceleration vs Time Y-axis")

    velocity_y = velocity(initial_velocity=0, acceleration=arr[:,2], time=arr[:,0])
    ayv.plot(arr[:,0], velocity_y)
    ayv.set_xlabel("Time (ms)")
    ayv.set_ylabel("Velocity (m/s)")
    ayv.set_title("Velocity vs Time Y-axis")

    position_y = position(initial_position=0, initial_velocity=0, velocity=velocity_y, time=arr[:,0])
    ayp.plot(arr[:,0], position_y)
    ayp.set_xlabel("Time (ms)")
    ayp.set_ylabel("Position (m) Y-Axis")
    axv.set_title("Time vs Position Y-axis")

    aza.plot(arr[:,0], arr[:,3])
    aza.set_xlabel("Time (ms)")
    aza.set_ylabel("Acceleration (m^2/s)")
    aza.set_title("Acceleration vs Time Z-axis")

    velocity_z = velocity(initial_velocity=0, acceleration=arr[:,3], time=arr[:,0])
    azv.plot(arr[:,0], velocity_z)
    azv.set_xlabel("Time (ms)")
    azv.set_ylabel("Velocity (m/s)")
    azv.set_title("Velocity vs Time Z-axis")

    position_z = position(initial_position=0, initial_velocity=0, velocity=velocity_z, time=arr[:,0])
    azp.plot(arr[:,0], position_z)
    azp.set_xlabel("Time (ms)")
    azp.set_ylabel("Position (m) Z-Axis")
    axv.set_title("Time vs Position X-axis")

    # # print(arr)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(arr[:,1], arr[:,2], arr[:,3])
    # ax.set_xlabel(header[1] + " (" + units[1] + ")")
    # ax.set_ylabel(header[2] + " (" + units[2] + ")")
    # ax.set_zlabel(header[3] + " (" + units[3] + ")")
    # plt.plot(arr[:,0], arr[:,1])
    plt.show()
if __name__ == "__main__":
    create_table("imu_data.csv")


