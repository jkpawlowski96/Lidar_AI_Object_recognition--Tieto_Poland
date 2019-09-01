"""Tools to display lidar -readings and assign label by button
label = LabelMaker(lidar)"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas
from matplotlib.figure import Figure
import numpy as np


class LabelMaker:
    def __init__(self, data):
        if data is None:
            lidar = []
        else:
            lidar = data
        self.lidar = lidar
        self.label = -1
        self.score()

    def score(self):
        app = QApplication(sys.argv)
        window = Window(self.lidar)
        window.show()
        app.exec()
        self.label = window.label


class Window(QMainWindow):
    def __init__(self, lidar):
        super().__init__()
        self.label = 0
        title = "Label maker"
        top = 400
        left = 400
        width = 400
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon("logo.png"))

        self.my_ui(lidar=lidar)

    def my_ui(self, lidar):
        canvas = Canvas(self, width=4, height=4, data=lidar)
        canvas.move(0, 0)
        # Button 1        self.setWindowIcon(QIcon("icon.png"))

        button = QPushButton("Ściana", self)
        button.clicked.connect(self.wall)
        button.move(20, 450)
        # Button 2
        button = QPushButton("Przeszkoda", self)
        button.clicked.connect(self.something)
        button.move(150, 450)
        # Button 3
        button = QPushButton("Pomiń", self)
        button.clicked.connect(self.skip)
        button.move(280, 450)

    """Buttons methods"""
    def wall(self):
        self.label = 0
        self.close()

    def something(self):
        self.label = 1
        self.close()

    def skip(self):
        self.label = -1
        self.close()


class Canvas(FingureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100, data=list):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FingureCanvas.__init__(self, fig)
        self.setParent(parent)

        plt = self.figure.add_subplot(111)
        """
        n = 180 / len(lidar)
        x = np.cos(np.linspace(0, 2 / n * np.pi, len(lidar)) + np.pi * 0.5 - np.pi * (1 / n))
        y = np.sin(np.linspace(0, 2 / n * np.pi, len(lidar)) + np.pi * 0.5 - np.pi * (1 / n))

        for i, reading in zip(range(len(lidar)), lidar):
            x[i] *= reading
            y[i] *= reading

        ax.scatter(x, y, s=5)  # lidar
        ax.scatter(0, 0, s=50)  # meshbot location
        """
        x = []
        y = []
        for yaw, lidar in zip(np.squeeze(np.asarray(data[0, :])),
                              np.squeeze(np.asarray(data[1, :]))):
            x.append(lidar * np.cos(2 * np.pi * yaw / 360))
            y.append(lidar * np.sin(2 * np.pi * yaw / 360))
        # lidar
        plt.scatter(x, y, s=5)
        # meshbot location
        plt.scatter(0, 0, s=50)


def chunk_it(seq, size, n_shuffle=0):
    out = []
    last = 0
    seq = seq.lidar
    while last+size < len(seq):
        out.append(seq[int(last):int(last + size)])
        last += size

    if n_shuffle > 0:
        for r in range(n_shuffle):
            r_step = np.random.randint(1, size - 1)
            last = r_step
            while last + size < len(seq):
                out.append(seq[int(last):int(last + size)])
                last += size
    return out
