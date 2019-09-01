from meshbotdata import MeshbotData
from label_maker import chunk_it, LabelMaker


def make_labels(filename):
    data = MeshbotData(filename)

    for chunk in data.slice(length=40, offset=20):
        label = LabelMaker(chunk).label

