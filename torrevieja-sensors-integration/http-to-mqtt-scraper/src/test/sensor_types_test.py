import unittest, sys, os, json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from main.sensor_data_parser import Measure, SensorInfo

class SensorInfoTest(unittest.TestCase):
    def test_equality(self):
        sensor1 = SensorInfo("sensor1", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")
        sensor2 = SensorInfo("sensor1", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")
        sensor3 = SensorInfo("sensor2", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")

        self.assertEqual(sensor1, sensor2)
        self.assertNotEqual(sensor1, sensor3)

    def test_hash(self):
        sensor1 = SensorInfo("sensor1", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")
        sensor2 = SensorInfo("sensor1", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")
        sensor3 = SensorInfo("sensor2", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")

        self.assertEqual(hash(sensor1), hash(sensor2))
        self.assertNotEqual(hash(sensor1), hash(sensor3))

class MeasureTest(unittest.TestCase):
    def test_to_json(self):
        sensor = SensorInfo("sensor1", "base64_sensor1", "name1", 1234567890, "lat1", "lon1", "alt1")
        measure = Measure(sensor, {"key1": "value1", "key2": "value2"})
        expected = {
            "sensor_info": {
                "location_id": "sensor1",
                "safe_location_id": "base64_sensor1",
                "name": "name1",
                "timestamp": 1234567890,
                "lat": "lat1",
                "lon": "lon1",
                "alt": "alt1"
            },
            "key1": "value1",
            "key2": "value2"
        }
        self.assertEqual(measure.toJSON(), json.dumps(expected))

if __name__ == '__main__':
    unittest.main()
