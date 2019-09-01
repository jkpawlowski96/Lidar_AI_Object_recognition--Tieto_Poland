### [Main page](./mainpage.md)   

# Connection
### Subsections

1. [Connection Method](#Conn)
2. [Orders](#ord)
3. [Interpreting Messages](#surr)

<a name="Conn"></a>
## 1. Connection Method

We connect to the meshbot by MQTT protocol. The connection is done by subscribing to "mqtt.tovity.com" topic and repeatedly checking if there is a new message from the robot.

<a name="ord"></a>
## 2. Orders


We give robot orders by sending specific messages to the same topic. For example to start scan or stop.

### **As of writing, those functions were not implemented in the application.**

We currently use help of Jankowski Krystian to directly give orders to robot.

## 3. Interpreting Messages
<a name="pars"></a>
Then the JSON is interpreted and transformed into a list of lidar readings.

<pre><code class="python">
def parser_thread(new_data, data_to_plot, data_to_predict):
    while demo_on:
        tmp = new_data.get()
        tmp.replace('\\n', '\n')
        tmp = tmp.replace('\\t', '\t')
        tmp = tmp[:-1]
        tmp = tmp[2:]
        d = json.loads(tmp)
        tmp += "\n * \n"
        lidar = sum([elem['lidar'] for elem in d['sensors']])
        print(lidar/len(d['sensors']))
        yaw = d['sensors'][0]['yaw']
        data_to_plot.put(item=[lidar/len(d['sensors']), yaw])
        data_to_predict.put({"lidar": lidar/len(d['sensors']), "yaw": yaw}) 

</code></pre>