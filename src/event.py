
"""
Event
Class representing humidity reading event
"""

import time
import uuid

class Event: # pylint: disable=C1001, R0903
    """
    Event
    Represents an sensor reading event
    """
    def __init__(self, humidity, temperature):
        self.event_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.humidity = humidity
        self.temperature = temperature

    def log(self):
        """
        log_event
        Prints an event's data to the console
        """
        print('Humidity: ', self.humidity)
        print('Temperature: ', self.temperature)
        print()
