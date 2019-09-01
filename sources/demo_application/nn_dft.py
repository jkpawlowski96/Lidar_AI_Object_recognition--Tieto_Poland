from DFT import DFTSpectrogram as dft
from nn_teacher import teach_nn
from save_load import save
import pandas as pd

def dft_teacher(layers, recursive=False):
    dft_data = pd.read_csv('../input/DFT_samples.csv')
    dft_X = dft_data.drop(columns=['Label'])
    dft_Y = dft_data.Label.values

    clf = teach_nn(dft_X.values, dft_Y, layers, recursive)

    model_name = 'mlpc_'

    for chunk in layers:
        model_name = model_name + '_' + str(chunk)

    save(clf, model_name, 'mlpc')

    return clf
