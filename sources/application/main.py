from queue import Queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import paho.mqtt.client as mqtt
import tensorflow as tf
import pandas as pd
import threading
import time
import numpy as np
import json
import datetime
from demo_application.save_load import load as load_model
from demo_application.plot_pred import score_yaw as acumulation

# neural network model
clf = load_model('mlpc_[500, 300, 200]_adam_300_0.01_100')

yaws = []

# matplotliba animation requires global variables
data_to_plot = Queue()
predictions = []
yaws_predicted = []

frame = ['''b'{\n\t"state":"IDLE",\n\t"battery":91,\n\t"sonar":960,\n\t"distance":30,\n\t"sensors":[\n\t{\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":300,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}, {\n\t\t"lidar":30,\n\t\t"ir":165,\n\t\t"yaw":''' + str(i) + '''\n\t}]\n}\'''' for i in range(360)]
demo_on = True

ready_to_predict = []



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("meshbot_dev/bot0/status")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global new_data
    new_data.put(item=str(msg.payload))


def mqtt_mock_thread(mqtt, new_data):
    i = 0
    while demo_on:
        time.sleep(1)
        new_data.put(frame[i])
        i += 1
        i %= 360


def mqtt_thread(mqtt, new_data):
    # mqtt client
    client = mqtt.Client("clientid-qwerty")
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("xxx", "yyy")
    client.connect("xxx", 123, 456)

    client.loop_forever()


def parser_thread(new_data, data_to_plot, data_to_predict):
    while demo_on:
        tmp = new_data.get()
        tmp = tmp.replace('\\n', '\n')
        tmp = tmp.replace('\\t', '\t')
        tmp = tmp[2:-1]
        d = json.loads(tmp)
        tmp += "\n * \n"
        lidar = sum([elem['lidar'] for elem in d['sensors']])
        yaw = d['sensors'][0]['yaw']
        raw = [lidar/len(d['sensors']), yaw]
        pos = process_data(raw)
        data_to_plot.put(pos)
        data_to_predict.put({"lidar": lidar/len(d['sensors']), "yaw": yaw})


def predict(data_frame):
    global clf
    data_frame = data_frame.copy()
    data = pd.DataFrame()
    i = 0
    for e in data_frame:
        data[str(i)] = [e]
        i += 1

    with tf.device('/cpu:0'):
        pred = clf.predict(data.values)[:, 1]
    # 0-1 probability
    return pred


def process_data(data):
    yaws.append(data[1])
    x = data[0] * np.cos(2 * np.pi * data[1] / 360)
    y = data[0] * np.sin(2 * np.pi * data[1] / 360)
    return x, y


# ploting
def plot_init():
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    return plots


# move processing to parser
def plot_update(frame):
    global data_to_plot
    global predictions
    global ready_to_predict
    while not data_to_plot.empty():
        pos = data_to_plot.get(True, timeout=None)
        xdata.append(pos[0])
        ydata.append(pos[1])
        ln.set_data(xdata, ydata)
    while not data_to_predict.empty():
        ready_to_predict.append(data_to_predict.get())
        if len(ready_to_predict) >= 40:
            lidar_readings = [item["lidar"] for item in ready_to_predict]
            yaws_for_prediction = []
            for item in ready_to_predict:
                yaws_for_prediction.append(item["yaw"])
            yaws_predicted.append(yaws_for_prediction)
            prediction = predict(lidar_readings)
            predictions.append(prediction)
            probabilities = acumulation(yaws_predicted, yaws, predictions)
            xdata_nn.clear()
            ydata_nn.clear()
            for yaw, probability in zip(yaws, probabilities):
                x = (10 * probability + 10) * np.cos(2 * np.pi * yaw / 360)
                y = (10 * probability + 10) * np.sin(2 * np.pi * yaw / 360)
                prediction_to_plot = (x, y)
                ready_to_predict = ready_to_predict[5:]
                xdata_nn.append(prediction_to_plot[0])
                ydata_nn.append(prediction_to_plot[1])
            ln_nn.set_data(xdata_nn, ydata_nn)
    return plots


if __name__ == '__main__':
    # matplotlib variables
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 2), ylim=(0, 100))
    xdata, ydata = [], []
    xdata_nn, ydata_nn = [], []
    ln = plt.plot([], [], 'bo', markersize=3)[0]
    ln_nn = plt.plot([], [], 'ro', markersize=2)[0]
    ln_bot = plt.plot([0], [0], 'go', markersize=5)[0]
    circle1 = plt.Circle((0, 0), 10, fill=False, color='g', label='Class "object 100%"')
    circle3 = plt.Circle((0, 0), 15, fill=False, color='0.7', label='Class object 50%')
    circle2 = plt.Circle((0, 0), 20, fill=False, color='g', label='Class "nothing"')
    plots = [ln_bot] + [ln] + [ln_nn]
    plt.gca().add_patch(circle1)
    plt.gca().add_patch(circle2)
    plt.gca().add_patch(circle3)

    # saviing readings for later
    file = open("samples" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt", "w")
    file.write("\n")

    new_data = Queue()
    data_to_predict = Queue()

    mqtt_th = threading.Thread(target=mqtt_thread, args=(mqtt, new_data))
    parser_th = threading.Thread(target=parser_thread, args=(new_data, data_to_plot, data_to_predict))

    parser_th.start()
    mqtt_th.start()
    time.sleep(5)
    ani = FuncAnimation(fig, plot_update, frames=720, interval=500, init_func=plot_init, blit=True)
    plt.show()

    demo_on = False

    parser_th.join()
