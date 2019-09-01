import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from preprocessing.meshbotdata import MeshbotData
from demo_application.nn_teacher import teach_nn, teach_conv_nn, data_conv
from demo_application.save_load import save as save_model
from demo_application.save_load import load as load_model
from lidar_readings.find import find_paths
from preprocessing.DFT import DFTSpectrogram as dft
from lidar_readings.test import test


def load(filename, gauss=0, interp=0, length=40, offset=2):
    data = MeshbotData(filename)
    if gauss > 0:
        data.gauss(gauss)
    if interp > 0:
        data.interpolate(interp)
    lidar_c = []
    yaw_c = []
    for chunk in data.slice(length, offset):
        lidar_c.append(np.asarray(chunk[1])[0:1][0])
        yaw_c.append(np.asarray(chunk[0])[0:1][0])
    return lidar_c, yaw_c, data


def score_yaw(yaw_chunks, yaws, preds):
    sum = list(np.zeros(max(yaws)+1))  # sum of pred for one yaw
    score = list(np.zeros(max(yaws)+1))
    for yaw_chunk, pred in zip(yaw_chunks, preds):
        yaw_chunk = [int(i) for i in yaw_chunk]
        for yaw in yaw_chunk:
            sum[yaw] += 1
            score[yaw] += pred

    for yaw in yaws:
        score[yaw] /= sum[yaw]
    return score


def pred_and_plot(clf, clf_type='mlpc', input_f=None, output_f=None):


    #df = pd.read_csv(input_f)
    #x_eval = df.drop(columns=['Label'])
    #y_eval = df.Label.values

    if clf_type=='mlpc':
        lidar_c, yaw_c, data = load(input_f, gauss=0.5, interp=5)
        lidar_c = np.asarray(lidar_c)
        y_pred = clf.predict_proba(lidar_c)[:, 1]

    if clf_type=='rnn':
        lidar_c, yaw_c, data = load(input_f, gauss=0.0, interp=0)
        lidar_c = np.asarray(lidar_c)
        lidar_c = np.reshape(lidar_c, (lidar_c.shape[0], 1, lidar_c.shape[1]))
        y_pred = clf.predict_proba(lidar_c)[:,0,1]

    if clf_type=='conv':
        lidar_c, yaw_c, data = load(input_f, gauss=0.0, interp=0)
        lidar_c = np.asarray(lidar_c)
        lidar_c = data_conv(lidar_c)
        y_pred = clf.predict_proba(lidar_c)[:, 1]

    if clf_type=='dft':
        lidar_c_dft, lidar_y = dft.load_from_csv(csv_name='../input/DFT_samples.csv')
        lidar_c_dft = np.asarray(lidar_c_dft)
        y_pred = clf.predict_proba(lidar_c_dft)[:, 1]

    label = score_yaw(yaw_c, data.yaw, y_pred)

    plot(data, label)

    if output_f is not None:
        pd.DataFrame({'y': y_pred}).to_csv(output_f, index=False)


def plot(data, label):
    fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    ax.axis('equal')
    size = 6
    fig.set_figheight(size)
    fig.set_figwidth(size)
    # lidar
    x = []
    y = []
    for yaw, lidar in zip(data.yaw, data.lidar):
        x.append(lidar * np.cos(2 * np.pi * yaw / 360))
        y.append(lidar * np.sin(2 * np.pi * yaw / 360))
    ax.scatter(x, y, c='b', s=5, label='lidar readings')


    ax.axis('equal')

    # pred
    x = []
    y = []

    r = 10

    for yaw in data.yaw:
        x.append((r * label[yaw] + r) * np.cos(2 * np.pi * yaw / 360))
        y.append((r * label[yaw] + r) * np.sin(2 * np.pi * yaw / 360))
    ax.scatter(x, y, c='r', s=3, label='Predict_proba accumulation')

    circle1 = plt.Circle((0, 0), r, fill=False, color='g', label='Class "object 100%"')
    circle3 = plt.Circle((0, 0), r * 1.5, fill=False, color='0.7', label='Class object 50%')
    circle2 = plt.Circle((0, 0), r * 2, fill=False, color='g', label='Class "nothing"')

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    # meshbot location
    ax.scatter(0, 0, c='m', s=80, label='Meshbot')
    #ax.legend(loc='lower right', markerscale=2)
    ax.legend(bbox_to_anchor=(0., -0.23, 1, 0), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)


    ax.title.set_text('Object detection around meshbot')
    ax.set_xlabel('X [cm]')
    ax.set_ylabel('Y [cm]')
    fig.show()


def main():
    files = test
    clf = load_model('..\models\mlpc_[500, 300, 200]_adam_300_0.01_100')
    for f in test:
        pred_and_plot(clf, clf_type='mlpc', input_f=f)


if __name__ == "__main__":
    main()
