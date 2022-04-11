import paho.mqtt.client as paho
import json
import schedule
import time

class Publish:
    def __init__(self):
        self.broker = "0.0.0.0"
        self.port = 1883
        self.client = paho.Client(client_id="teststand",clean_session=True,userdata=None,protocol=paho.MQTTv311,transport="tcp")
        self.client.username_pw_set(username="nakuja",password="aVesSaVQVKjE8JCKrpTEheYERDWdfM")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker, self.port, 10)
        print("Connected")

    def on_connect(self, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("test")


    def on_publish(self, userdata, msg):
        # print(f"Published msg: {msg}")
        pass

    def publish(self, data):
        topic = f"sensorData/teststand"
        pub_data = {
            "time": time.localtime(),
            "data": data,
        }
        msg = json.dumps(pub_data)
        self.client.publish(topic, msg)