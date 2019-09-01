import pandas as pd


def load_meshbot_lidar(file_name):
    """function returns training and testing data sets"""
    raw_data = pd.read_csv(file_name)

    y = raw_data['Label'].values
    x = raw_data.drop('Label', axis=1).values

    return x, y
