from paho.mqtt import client as mqtt_client
from logging import getLogger

logger = getLogger(__name__)

def connect_mqtt(broker: str, port: int) -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
