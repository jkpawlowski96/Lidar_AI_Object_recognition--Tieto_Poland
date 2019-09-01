import matplotlib.pyplot as plt
import numpy as np
from sources.preprocessing.meshbotdata import MeshbotData
import matplotlib.pyplot as plt


def plot_file(filename, gauss=0, interpolation=0):
    data = MeshbotData(filename)
    if gauss > 0:
        data.gauss(gauss)
    if interpolation > 0:
        data.interpolate(interpolation)
    plot_lidar(data)


def plot_file_sliced(filename, gauss=0, length=40, offset=20):
    data = MeshbotData(filename)
    if gauss > 0:
        data.gauss(gauss)
    for chunk in data.slice(length, offset):
        plot_from_matrix(chunk)


def plot_lidar(data):
    x = []
    y = []
    for yaw, lidar in zip(data.yaw, data.lidar):
        x.append(lidar * np.cos(2 * np.pi * yaw / 360))
        y.append(lidar * np.sin(2 * np.pi * yaw / 360))
    # lidar
    plt.scatter(x, y, s=5)
    # meshbot location
    plt.scatter(0, 0, s=50)
    plt.show()


def plot_from_matrix(data):
    x = []
    y = []
    for yaw, lidar in zip(np.squeeze(np.asarray(data[0, :])),
                          np.squeeze(np.asarray(data[1, :]))):
        print(yaw)
        x.append(lidar * np.cos(2 * np.pi * yaw / 360))
        y.append(lidar * np.sin(2 * np.pi * yaw / 360))
    # lidar
    plt.scatter(x, y, s=5)
    # meshbot location
    plt.scatter(0, 0, s=50)
    plt.show()

