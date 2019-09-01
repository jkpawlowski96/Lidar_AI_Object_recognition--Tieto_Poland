import json


def json_load(filename):
    """Reads JSON file and returns list of objects"""

    # open first file
    with open(filename, 'r') as f:
        data = f.read()

    # split by *
    data = data.split("*")[:-1]
    print(data)

    packs = len(data)  # last is blanc
    print('Loaded packs from file:', packs)

    jsons_list = []  # jsons
    for reading in data:
        # load one json
        pack = json.loads(reading)
        # add json into list
        jsons_list.append(pack)

    return jsons_list

