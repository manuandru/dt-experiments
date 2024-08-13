import os, requests
import time
from sensor_data_parser import parse_response_data
from mqtt_client import connect_mqtt
from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


HTTP_ENDPOINTS = os.environ.get(
    'HTTP_ENDPOINTS',
    "http://localhost:3000/buoy,http://localhost:3000/weather"
)
SLEEP_TIME_SECONDS = os.environ.get('SLEEP_TIME', 10)
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'localhost')
MQTT_PORT = os.environ.get('MQTT_PORT', 1883)

if __name__ == '__main__':

    client = connect_mqtt(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    endpoints = HTTP_ENDPOINTS.split(',')

    while True:

        for endpoint in endpoints:
            logger.info(f"Fetching data from {endpoint}")
            try:
                response = requests.get(endpoint, verify=False).json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching data from {endpoint}: {e}")
                continue
            response = requests.get(endpoint, verify=False).json()
            measures = parse_response_data(response)
            for measure in measures:
                client.publish(
                    f"sensors/{measure.sensor_info.safe_location_id}",
                    measure.toJSON(),
                    qos=1
                )

        time.sleep(SLEEP_TIME_SECONDS)
