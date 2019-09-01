from preprocessing.lidardata import separate_yaw_lidar_from_json
from scipy import ndimage, interpolate, signal
import numpy as np


class MeshbotData:
    """holds lidar readings and reading angle in two lists"""

    def __init__(self, filename='log.txt'):
        self.yaw, self.lidar = separate_yaw_lidar_from_json(filename)
        self.mean()

    def gauss(self, gauss):
        self.lidar = ndimage.gaussian_filter(self.lidar, gauss, 0, None, 'wrap')
        self.mean()

    def interpolate(self, max_empty_space=5):
        """
        Interpolate readings
        :param max_empty_space: how many readings can by interpolate in one place
        :return:
        """
        f = interpolate.interp1d(self.yaw, self.lidar)
        end = self.yaw[len(self.yaw)-1]
        lidar = []
        yaw = []
        new_readings = 0
        for angle in range(0, end):
            if angle in self.yaw:
                yaw.append(angle)
                lidar.append(f(angle))
                new_readings = 0
            else:
                if new_readings > max_empty_space:
                    continue
                yaw.append(angle)
                lidar.append(f(angle))
                new_readings = new_readings + 1
        self.lidar = lidar
        self.yaw = yaw
        self.mean()

    def mean(self):
        lidar = []
        yaw = []
        for angle in range(360):
            lidar_value = []
            if self.yaw.count(angle) == 0:
                continue

            index = [i for i, x in enumerate(self.yaw) if x == angle]
            for i in index:
                lidar_value.append(self.lidar[i])

            yaw.append(angle)
            lidar.append(np.mean(lidar_value))

        self.lidar = lidar
        self.yaw = yaw

    def slice(self, length, offset=0):
        i = 0
        end = len(self.lidar) - length
        if max(self.yaw) - min(self.yaw) > 356:
            i = -length + 1
        while i < end:
            frame_end = i + length
            yaw = circular_range(self.yaw, i, frame_end)
            lidar = circular_range(self.lidar, i, frame_end)
            yield np.matrix([yaw, lidar])
            i += offset


def circular_range(collection, start, end, step=1):
    if start < 0:
        return collection[start::step] + collection[:end:step]
    else:
        return collection[start:end:step]
