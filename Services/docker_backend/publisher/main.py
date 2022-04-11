import paho.mqtt.client as paho
import json
import schedule
import time

TIME_PERIOD: float = 0.001


class TestPublisher:
    def __init__(self):
        """
        Initializes the Publisher class

        :rtype: None
        """
        self.MQTT_ADDRESS = '127.0.0.1'
        self.MQTT_PORT = 1883
        self.MQTT_USER = 'nakuja'
        self.MQTT_PASSWORD = 'aVesSaVQVKjE8JCKrpTEheYERDWdfM'
        self.MQTT_CLIENT = 'publisher'

        self.client = None
        self.counter = 0
        self.time_to_run = 0
        self.published_count = 0

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        This is to handle this the on_connect callback before you create the connection.
        RC types:
        0: Connection successful
        1: Connection refused – incorrect protocol version
        2: Connection refused – invalid client identifier
        3: Connection refused – server unavailable
        4: Connection refused – bad username or password
        5: Connection refused – not authorised
        :param client: This is a client object.
        :param userdata: The private user data as set in Client()
        :param flags: response flags sent by the broker
        :param rc: Return Code is used for checking that the connection was established.
        :type client: str
        :type userdata: str
        :type flags: dict
        :type rc: str
        :rtype: None
        """
        print("Connected with result code " + str(rc))

    def on_publish(self, client, userdata, msg):
        """
        Called when a message has been received on a topic
        :param client: This is a client object.
        :param userdata: The private user data as set in Client()
        :param msg: an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        :type client: str
        :type userdata: str
        :type msg: class
        :rtype: None
        """
        self.published_count = self.published_count + 1
        if self.published_count == 2000:
            self.published_count = 0
            print("Published 2000 messages")

    def setup(self):
        """
        This setups up the MQTT client
        :rtype None:
        """
        self.client = paho.Client(client_id=self.MQTT_CLIENT, clean_session=True,
                                  userdata=None, protocol=paho.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        self.client.username_pw_set(username=self.MQTT_USER, password=self.MQTT_PASSWORD)
        self.client.connect(self.MQTT_ADDRESS, self.MQTT_PORT, 10)

    def run(self):
        """
        This runs the publisher
        :rtype None:
        """
        start = time.time()
        data = 120 + self.counter
        topic = "sensorData/teststand"
        pub_data = {
            "time": time.ctime(),
            "data": data,
            "frequency": 1 / TIME_PERIOD,
            "time_to_run": self.time_to_run
        }
        msg = json.dumps(pub_data)
        self.client.publish(topic, msg)
        self.counter = self.counter + 1
        if self.counter == 10:
            self.counter = 0
        end = time.time()
        self.time_to_run = end - start


demo = TestPublisher()
demo.setup()
schedule.every(TIME_PERIOD).seconds.do(demo.run)

while True:
    schedule.run_pending()
    time.sleep(TIME_PERIOD)
