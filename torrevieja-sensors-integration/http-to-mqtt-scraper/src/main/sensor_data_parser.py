import json
from base64 import b64encode
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

type SensorsMeasurements = dict[SensorInfo, dict[str, str]]

@dataclass(frozen=True)
class SensorInfo:
    """
    Represents the information of a sensor.
    """
    location_id: str            # <sensorId>_<name>_<lat>_<lon>_<alt>
    safe_location_id: str
    name: str
    timestamp: int              # Unix ms timestamp
    lat: str
    lon: str
    alt: str

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SensorInfo) and value.location_id == self.location_id
    
    def __hash__(self) -> int:
        return hash(self.location_id)

class Measure:
    """
    Represents a measure of a sensor, containing the sensor info and the data related to the measure.
    """
    def __init__(self, sensor_info: SensorInfo, measure_data: dict):
        self.sensor_info = sensor_info
        self.measure_data = measure_data
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Measure) and value.sensor_info == self.sensor_info
    
    def __hash__(self) -> int:
        return hash(self.sensor_info)

    def __repr__(self) -> str:
        return f"Measure(sensor_info={self.sensor_info}, measure_data={self.measure_data})"

    def toJSON(self):
        return json.dumps({
            'sensor_info': self.sensor_info.__dict__,
            **self.measure_data
        })
        
def parse_response_data(response: any) -> set[Measure]:
    """
    Parses the response data from the HTTP endpoint and returns a set of measures.
    """
    sensors_data: SensorsMeasurements = {}
    for data in response['data']:
        
        if 'location_id' not in data \
            or 'name' not in data \
            or 'timestamp' not in data \
            or 'lat' not in data \
            or 'lon' not in data \
            or 'alt' not in data \
            or 'sensor_type' not in data \
            or 'value' not in data:
            logger.error(f"Invalid data, missing fields.")
            continue

        sensor_info = SensorInfo(
            location_id=data['location_id'],
            safe_location_id=b64encode(data['location_id'].encode()).decode(),
            name=data['name'],
            timestamp=data['timestamp'],
            lat=data['lat'],
            lon=data['lon'],
            alt=data['alt']
        )
        if sensor_info not in sensors_data:
            sensors_data[sensor_info] = {}
        sensors_data[sensor_info][data['sensor_type']] = data['value']
    
    measures = set()
    for sensor_info, data in sensors_data.items():
        measures.add(Measure(sensor_info, data))
    return measures
