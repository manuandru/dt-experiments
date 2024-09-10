# Torrevieja Injector - HTTP scraper to MQTT

This is an Injector module that reads data from HTTP endpoints and publishes it to MQTT broker. The module specifies the mapping function that is used to map the data from the HTTP source to the MQTT message payload.

## Configuration

The module is configured using the following environment variables:

- `HTTP_ENDPOINTS`: The HTTP endpoints to poll for data. The endpoints are separated by commas.
- `HTTP_POLL_INTERVAL_SECONDS`: The interval in seconds to poll the HTTP endpoints.
- `MQTT_BROKER`: The MQTT broker to publish the data to.
- `MQTT_PORT`: The MQTT broker port.

## Mapping Function

The mapping function transforms data from the HTTP source (the project's JSON data source), merging together more data points from the same source and same timestamp, mapping into JSON payload. Here is an example:

Source data:

```json
[
    {
        "location_id": "<sensor-id>",
        "name": "<sensor-name>",
        "lat": "<lat>",
        "lon": "<lon>",
        "alt": "<alt>",
        "sensor_type": "<sensor-type1>",
        "value": "<value1>",
        "timestamp": "<timestamp>"
    },
    {
        "location_id": "<sensor-id>",
        "name": "<sensor-name>",
        "lat": "<lat>",
        "lon": "<lon>",
        "alt": "<alt>",
        "sensor_type": "<sensor-type2>",
        "value": "<value2>",
        "timestamp": "<timestamp>"
    }
]
```

Output data:

```json
{
    "sensor_info": {
        "location_id": "<sensor-id>",
        "safe_location_id": "base64(<sensor-id>)",
        "name": "<sensor-name>",
        "timestamp": "<timestamp>",
        "lat": "<lat>",
        "lon": "<lon>",
        "alt": "<alt>"
    },
    "<sensor-type1>": "<value1>",
    "<sensor-type2>": "<value2>"
}
```

## Deployment

The module is deployed as a Docker container. The Docker image is built using the `Dockerfile` in the root of the project. The image is published to `DockerHub`, in [manuandru/torrevieja-http-to-mqtt-scraper](https://hub.docker.com/r/manuandru/torrevieja-http-to-mqtt-scraper) repository.

The module could be deployed using the following `docker-compose.yaml` file and the following command:

```bash
docker compose up -d
```

## Development

The module is developed using Python 3. The module is implemented in the `main.py` file. The module uses the `requests` library to poll the HTTP endpoints and the `paho-mqtt` library to connect to the MQTT broker.

The module is tested using the `unittest` library. The tests are implemented in the `test_main.py` file.

For development, the module could be run using the `develop` submodule that simulate the HTTP endpoints an example of data and the MQTT broker. The development environment could be started using the following command:

```bash
cd develop
docker compose up
```

The docker compose file for the development environment uses the compose watch feature to restart the container when the source code changes.
