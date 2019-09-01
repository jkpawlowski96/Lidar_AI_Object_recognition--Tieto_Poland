from queue import Queue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading as td
import time
from preprocessing.meshbotdata import MeshbotData
import signal


def data_simulate(reading, num):
    data = MeshbotData('../lidar-readings/m3_1cm.txt')
    for yaw, lidar in zip(data.yaw, data.lidar):
        reading.put(item=[lidar * np.cos(2 * np.pi * yaw / 360), lidar * np.sin(2 * np.pi * yaw / 360)])
        time.sleep(1)


def init():
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    return ln,


def update(frame):
    global reading
    global prediction
    while not reading.empty():
        pos = reading.get(True, timeout=None)
        xdata.append(pos[0])
        ydata.append(pos[1])
        ln.set_data(xdata, ydata)
    while not prediction.empty():
        pos = prediction.get(True, timeout=None)
        xdata.append(pos[0])
        ydata.append(pos[1])
        ln.set_data(xdata, ydata)
    return ln,


reading = Queue()
prediction = Queue()


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

simj = td.Thread(group=None, target=data_simulate, args=(reading, 0))
simj.start()
ani = FuncAnimation(fig, update, frames=720, interval=500, init_func=init, blit=True)
plt.show()

simj.join()
