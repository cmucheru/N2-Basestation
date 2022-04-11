import paho.mqtt.client as paho
import json
import time


# TODO place in utils folder
class Publisher:
    def __init__(self, logger):
        """
        Initializes the Publisher class

        :rtype: None
        """
        self.MQTT_ADDRESS = '127.0.0.1'
        self.MQTT_PORT = 1883
        self.MQTT_USER = 'nakuja'
        self.MQTT_PASSWORD = 'aVesSaVQVKjE8JCKrpTEheYERDWdfM'
        self.MQTT_CLIENT = 'teststandapi'

        self.client = None
        self.logger = logger
        self.setup()

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
        self.logger.info("Connected with result code " + str(rc))

    def on_publish(self, client, userdata, message):
        """
        Called when a message has been received on a topic
        It will log and information after 2000 published messages
        :param client: This is a client object.
        :param userdata: The private user data as set in Client()
        :param message: an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        :type client: str
        :type userdata: str
        :type message: class
        :rtype: None
        """
        self.logger.info("Published message : {}".format(message))

    def setup(self):
        self.client = paho.Client(client_id=self.MQTT_CLIENT, clean_session=True, userdata=None, protocol=paho.MQTTv311,
                                  transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.username_pw_set(
            username=self.MQTT_USER, password=self.MQTT_PASSWORD)
        self.client.connect(self.MQTT_ADDRESS, self.MQTT_PORT, 10)
        self.logger.info("CONNECTED TO MQTT")

    def publish(self, data):
        topic = "sensorData/internals"
        pub_data = {
            "time": time.ctime(),
            "data": data,
        }
        msg = json.dumps(pub_data)
        self.client.publish(topic, msg)


class Operation:
    def __init__(self, logger):
        self.ignition = False
        self.logging = False
        self.publisher = Publisher(logger)
        self.logger = logger

    def startignition(self):
        """
        Start Ignition
        """
        if self.ignition:
            response = {"message": "Ignition already started",
                        "ignition status": str(self.ignition)}
        else:
            if self.logging:
                self.ignition = True
                response = {"message": "Started ignition",
                            "ignition status": str(self.ignition)}
                self.logger.info("Started ignition")
                self.publisher.publish(data=response)
            else:
                response = {"message": "Start logging first",
                            "redirect": "/api/start_logging"}
        return response

    def stopignition(self):
        """
        Stops Ignition
        """
        if self.ignition:
            if self.logging:
                response = {"message": "Stop logging first",
                            "redirect": "/api/stop_logging"}
            else:
                self.ignition = False
                response = {"message": "Stopped ignition",
                            "ignition status": str(self.ignition)}
                self.logger.info("Stopped ignition")
                self.publisher.publish(data=response)
        else:
            response = {"message": "Ignition not started",
                        "ignition status": str(self.ignition)}
        return response

    def startlogging(self):
        """
        Start logging
        """
        if not self.logging:
            self.logging = True
            response = {"message": "Started logging",
                        "logging status": str(self.logging)}
            self.logger.info("Started logging")
            self.publisher.publish(data=response)
        else:
            response = {"message": "Logging already started",
                        "logging status": str(self.logging)}
        return response

    def stoplogging(self):
        """
        Stops logging
        """
        if self.logging:
            self.logging = False
            response = {"message": "Stopped logging",
                        "logging status": str(self.logging)}
            self.logger.info("Stopped logging")
            self.publisher.publish(data=response)
        else:
            response = {"message": "Logging already stopped",
                        "logging status": str(self.logging)}
        return response
