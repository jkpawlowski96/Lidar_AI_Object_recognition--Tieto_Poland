"""Tools to create data input for ai"""

from preprocessing.label_maker import chunk_it, LabelMaker
from preprocessing.meshbotdata import MeshbotData
import pandas as pd
import numpy as np
import glob
import os
from input.test import test as test_files
from input.test import test_prep as test_files_prep


def datascore(filename, prep=False):
    """
    Save chunk readings as .csv, file name from path
    :param filename: readings
    :return: path to file .csv
    """
    part_size = 40  # size of window
    step = 5       # size of move to next window
    d = {}
    for i in range(part_size):
        col = 'Lidar'+str(i)
        d.update({col: 'int8'})
    d.update({'Label': 'int8'})

    meshbot_data = MeshbotData(filename)

    if prep:
        meshbot_data.interpolate(5)
        meshbot_data.gauss(0.5)
    data = []
    parts = meshbot_data.slice(length=part_size, offset=step)
    for part in parts:
        label = LabelMaker(part).label
        # skip line in file
        if label == -1:
            continue
        part = part.tolist()[1]
        part.append(label)
        data.append(part)

    data = pd.DataFrame(data=data, columns=d)
    filename = filename.split('/')[2].split('.')[0]  # filename from path
    # Save dataframe
    if prep:
        path=data.to_csv('../input/'+filename+'_prep.csv', index=False)
    else:
        path=data.to_csv('../input/'+filename+'.csv', index=False)
    return path


def merge_to_maindata(preprocessed=False):
    '''

    :param preprocessed: If true merge preprocesed data
    :return:
    '''
    if preprocessed:
        files = glob.glob("../input/*prep.csv")
    else:
        files = glob.glob("../input/*.csv")
    if preprocessed:
        to_remove=['../input\\Merged_prep.csv', '../input\\train_prep.csv', '../input\\test_prep.csv']
    else:
        to_remove=['../input\\Merged.csv', '../input\\train.csv', '../input\\test.csv']
    for f in to_remove:
        if f in files:
            files.remove(f)

    if preprocessed:
        test = test_files_prep
    else:
        test = test_files

    train = files.copy()
    for f in test:
        train.remove(f)

    df = pd.concat((pd.read_csv(f, header=0) for f in files), sort=False, ignore_index=True)
    df_deduplicated = df.drop_duplicates()

    if preprocessed:
        df_deduplicated.to_csv("../input/Merged_prep.csv", index=False)
    else:
        df_deduplicated.to_csv("../input/Merged.csv", index=False)

    df = pd.concat((pd.read_csv(f, header=0) for f in train), sort=False, ignore_index=True)
    df_deduplicated = df.drop_duplicates()

    if preprocessed:
        df_deduplicated.to_csv("../input/train_prep.csv", index=False)
    else:
        df_deduplicated.to_csv("../input/train.csv", index=False)

    df = pd.concat((pd.read_csv(f, header=0) for f in test), sort=False, ignore_index=True)
    df_deduplicated = df.drop_duplicates()

    if preprocessed:
        df_deduplicated.to_csv("../input/test_prep.csv", index=False)
    else:
        df_deduplicated.to_csv("../input/test.csv", index=False)
