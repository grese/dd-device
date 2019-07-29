
"""
SensorData
Class containing humidity/temp data from sensor reading
"""

import time
import uuid

class SensorData: # pylint: disable=C1001, R0903
    """
    SensorData
    Represents a sensor reading
    """
    def __init__(self, humidity, temperature):
        self.data_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.humidity = humidity
        self.temperature = temperature

    def log_data(self):
        """
        log
        Prints an sensor data to the console
        """
        print('Humidity: ', self.humidity)
        print('Temperature: ', self.temperature)
        print()

    def to_dict(self):
        """
        to_json
        returns sensor data data as dictionary
        """
        return {
            "data_id": self.data_id,
            "timestamp": self.timestamp,
            "humidity": self.humidity,
            "temperature": self.temperature
            }
