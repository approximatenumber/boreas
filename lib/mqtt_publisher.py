import paho.mqtt.client as mqtt_client
import logging

logger = logging.getLogger('boreas')


class MQTTPublisher():

    BROKER_HOST = 'localhost'
    NAME = "BOREAS"
    ROOT_TOPIC = 'boreas'

    def __init__(self):
        self.client = mqtt_client.Client(self.NAME)
        self.client.connect(self.BROKER_HOST)

    def publish(self, topic: str, value: int):
        self.client.publish(f"/{self.ROOT_TOPIC}/{topic}", value)
