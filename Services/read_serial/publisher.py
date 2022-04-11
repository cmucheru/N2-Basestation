import paho.mqtt.client as paho
import json
import time

TIME_PERIOD: float = 0.0125


# TODO place in utils folder
class TestPublisher:
    def __init__(self, logger):
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
        self.time_to_run = 0
        self.published_count = 0
        self.logger = logger
        self.setup()
        self.lastmessage = None

    def on_connect(self, client, userdata, flags, rc):
        """
        This is to handle this the on_connect callback before you create the connection.
        It will subscribe to the "sensorData/internals" topic upto connecting to the message broker
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
        self.client.subscribe("sensorData/internals")
        self.logger.info("Connected to rabbitmq with result code " + str(rc))

    def on_publish(self, client, userdata, msg):
        """
        Called when a message has been received on a topic
        It will log and information after 2000 published messages
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
            self.logger.info("[{}] Published 2000 messages".format(time.ctime()))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        Called when a message has been received on a topic
        :param client: This is a client object.
        :param userdata: The private user data as set in Client()
        :param granted_qos: This is a list of integers that give the QoS level the broker has granted for the request
        :type client: str
        :type userdata: str
        :type mid: str
        :type granted_qos: str
        :rtype: None
        """
        self.logger.info("SUBSCRIBED: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, message):
        """
        Callback that will be used for each message received

        :param client: This is a client object.
        :param userdata: The private user data as set in Client()
        :param message: An instance of MQTTMessage
        :type client: str
        :type userdata: str
        :type message: class
        :return:
        """
        self.logger.info("Received message from {}".format(message.topic))
        self.lastmessage = str(message.payload.decode("utf-8"))

    def setup(self):
        """
        This setups up the MQTT client
        :rtype None:
        """
        self.client = paho.Client(client_id=self.MQTT_CLIENT, clean_session=True, userdata=None, protocol=paho.MQTTv311,
                                  transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.loop_start()

        self.client.username_pw_set(username=self.MQTT_USER, password=self.MQTT_PASSWORD)
        # TODO wrap connect in try except block
        self.client.connect(self.MQTT_ADDRESS, self.MQTT_PORT, 10)

    def run(self, data):
        """
        This runs the publisher
        :rtype None:
        """
        start = time.time()
        topic = "sensorData/teststand"
        pub_data = {
            "time": time.ctime(),
            "data": float(data),
            "frequency": 1 / TIME_PERIOD,
            "time_to_run": self.time_to_run
        }
        msg = json.dumps(pub_data)
        self.client.publish(topic, msg)
        end = time.time()
        self.time_to_run = end - start

    @property
    def check_message(self):
        """
        Returns the last message available
        :rtype: str
        """
        return self.lastmessage
