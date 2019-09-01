import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading as td
import time
from preprocessing.meshbotdata import MeshbotData

x_buff, y_buff = [], []
block = td.Event()
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')


def init():
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    return ln,


def update(frame):
    block.wait()
    block.clear()

    xdata.append(x_buff[frame-1])
    ydata.append(y_buff[frame-1])
    ln.set_data(xdata, ydata)
    return ln,


def download_from_meshbot():
    data = MeshbotData('../lidar-readings/m3_1cm.txt')
    for yaw, lidar in zip(data.yaw, data.lidar):
        x_buff.append(lidar * np.cos(2 * np.pi * yaw / 360))
        y_buff.append(lidar * np.sin(2 * np.pi * yaw / 360))
        block.set()
        time.sleep(1)


read_data = td.Thread(target=download_from_meshbot)


# TODO read data from meshbot


# TODO classify

# TODO plot
read_data.start()

ani = FuncAnimation(fig, update, frames=[frame for frame in range(360)],
                    init_func=init, blit=True)
plt.show()

print("got")
read_data.join()
