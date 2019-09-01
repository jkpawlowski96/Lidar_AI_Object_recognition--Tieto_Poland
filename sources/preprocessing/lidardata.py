import preprocessing.json_load as jl


class LidarData:
    """Read JSON list and returns lidar and yaw data """
    def __init__(self, jsons_list=None):
        # Lidar Data
        if jsons_list is None:
            jsons_list = []
        self.data = list()
        # Unpack JSONS
        for pack in jsons_list:
            sensors = pack['sensors']
            # Copy all measures
            for measure in sensors:
                # Lidar nad Yaw data from JSON list
                self.data.append([measure['lidar'], measure['yaw']])


def separate_yaw_lidar_from_json(filename):
    """Read JSON file and returns two lists: lidar and yaw data """
    lidar_distance = list()
    yaw = list()

    json_data = jl.json_load(filename)
    x = LidarData(json_data)
    for reading in x.data:
        if reading[1] > 179:
            reading[1] = (reading[1] % 65355)+180
        if reading[0] != 65535:
            if len(yaw) == 0:
                lidar_distance.append(reading[0])
                yaw.append(reading[1])
                continue
            if yaw[len(yaw)-1] == reading[1]:
                lidar_distance[len(lidar_distance)-1] = ((reading[0] + lidar_distance[len(lidar_distance) - 1]) / 2)
            else:
                lidar_distance.append(reading[0])
                yaw.append(reading[1])

    if len(yaw) != len(lidar_distance):
        print("SOMETHING IS VERY WRONG!")
        return -1

    # Gives two lists contating current angle between 0-359 and distance
    return yaw, lidar_distance
