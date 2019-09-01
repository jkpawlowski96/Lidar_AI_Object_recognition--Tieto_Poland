from demo_application.plot_pred import pred_and_plot
from demo_application.nn_teacher import teach_nn, teach_conv_nn, data_conv
import pandas as pd
import numpy as np
from demo_application.save_load import save
from demo_application.save_load import load as load_model
from lidar_readings.test import test as test_files

from demo_application.metrics import score
import csv


def df_xy(filename):

    X = pd.read_csv(filename)
    y = X.Label.values
    X.drop(columns=['Label'], inplace=True)
    return X.values, y


def new_nn(type='conv'):
    if type=='conv':
        X_train, y_train = df_xy('../input/train.csv')
        X_test, y_test = df_xy('../input/test.csv')
    if type=='mlpc':
        X_train, y_train = df_xy('../input/train_prep.csv')
        X_test, y_test = df_xy('../input/test_prep.csv')

    param={
            'layers': [500, 300, 200, 100],
            #'kernel': 12,
            'optimizer': 'adam',
            'epochs': 400,
            'learning_rate': 0.0005,
            'batch': 200
        }

    if type == 'conv':
        clf = teach_conv_nn(X_train, y_train,
                            layers=param['layers'],
                            optimizer=param['optimizer'],
                            epochs=param['epochs'],
                            learning_rate=param['learning_rate'],
                            batch=param['batch'],
                            kernel=param['kernel'])
        X_test = data_conv(X_test)
    if type == 'mlpc':
        clf = teach_nn(X_train, y_train,layers=param['layers'],
                            optimizer=param['optimizer'],
                            epochs=param['epochs'],
                            learning_rate=param['learning_rate'])

    modelname = type
    for p in param.values():
        modelname += '_'+str(p)

    f1, balanced_accuracy, auc, null = score_model(clf, X_test, y_test)

    param['F1'] = f1
    param['balanced_accuracy'] = balanced_accuracy
    param['auc'] = auc
    param['null'] = null

    if type=='conv':
        scorefile='../models/scored_conv.csv'
    if type =='mlpc':
        scorefile='../models/scored_mlpc.csv'

    with open(scorefile, 'a', newline='') as csvfile:
        fieldnames = param.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(param)

    save(clf, modelname, type)

    return clf


def score_model(model,X_test,y_test):
    y_pred = model.predict(X_test)[:, 1].ravel()
    y_pred = np.round(y_pred)
    f1, balanced_accuracy, auc, null = score(y_test, y_pred)
    print('F1', f1)
    print('balanced_accuracy', balanced_accuracy)
    print('AUC', auc)
    print('null', null)
    return f1, balanced_accuracy, auc, null

def score_model_test(clf,type='conv'):
    if type=='conv':
        X_test, y_test = df_xy('../input/test.csv')
        X_test = data_conv(X_test)
    if type=='mlpc':
        X_test, y_test = df_xy('../input/test_prep.csv')

    y_pred = clf.predict(X_test)[:,1]
    y_pred=np.round(y_pred)
    score(y_test,y_pred)

clf = load_model('mlpc_[500, 300, 200]_adam_300_0.01_100')
score_model_test(clf, type='mlpc')

