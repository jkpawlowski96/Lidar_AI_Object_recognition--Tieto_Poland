import matplotlib.pyplot as plt
import numpy as np
from sources.preprocessing.meshbotdata import MeshbotData
from scipy import signal
import pandas as pd

class DFTSpectrogram:

    sett = list()

    def __init__(self, window_samples=None, n_overlap=None, window_name=None, scaling=None):
        self.sett.append(window_samples)
        self.sett.append(window_name)
        self.sett.append(n_overlap)
        self.sett.append(scaling)

    def dft_yaw(self, data):
        new_data = np.array(data.lidar)
        f, t, Sxx = signal.spectrogram(new_data,
                                       fs=self.sett[0],
                                       window=signal.get_window(self.sett[1], Nx=self.sett[0]),
                                       noverlap=self.sett[2],
                                       scaling=self.sett[3])
        return f, t, Sxx

    def plot_dft(self, filename):
        if len(self.sett) is 0:
            print("Err: No settings")

        else:
            data = MeshbotData(filename)
            print("Lidar data length: ",len(data.lidar))
            f, t, Sxx = self.dft_yaw(data)
            print("Time series length:", len(t))
            self.plot_dft_yaw(f, t, Sxx)

    def plot_dft_yaw(self, f, t, Sxx):
        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('Frequency')
        plt.xlabel('Samples')
        plt.show()

    def get_sectrogram_data(self, filename):
        vecSxx = list()
        if len(self.sett) is 0:
            print("Err: No settings")

        else:
            data = MeshbotData(filename)
            f, t, Sxx = self.dft_yaw(data)
            for i in Sxx:
                for a in i:
                    vecSxx.append(a)
        return vecSxx

    def load_from_csv(self, csv_name):
        dft_data = pd.read_csv(csv_name)
        dft_X = dft_data.drop(columns=['Label'])
        dft_Y = dft_data.Label.values

        return  dft_X, dft_Y

    def dft_from_modules(self, csv_name, plot = False):
        # How to choose length of window:
        # n_window = ((n_samples - (n_result-1)*n_overlap) - 1 +n_result^2)/n_result

        dft_X, dft_Y = self.load_from_csv(csv_name)

        d = {}
        data = []
        vec_data = []

        iter = 0

        for i in dft_X.values:
            tmp_vec = []
            f, t, Sxx = signal.spectrogram(i,
                                           fs=self.sett[0],
                                           window=signal.get_window(self.sett[1], Nx=self.sett[0]),
                                           noverlap=self.sett[2],
                                           scaling=self.sett[3])
            if plot is True:
                self.plot_dft_yaw(f, t, Sxx)
            for j in Sxx:
                for k in j:
                    tmp_vec.append(k)

            tmp_vec.append(dft_Y[iter])
            vec_data.append(tmp_vec)
            iter = iter + 1

        for i in range(len(vec_data[0])-1):
            col = 'Lidar' + str(i)
            d.update({col: 'int8'})
        d.update({'Label': 'int8'})

        data = pd.DataFrame(data=vec_data, columns=d)

        data.to_csv('../input/DFT_samples.csv', index=False)



        
