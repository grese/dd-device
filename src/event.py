
"""
Event
Class representing humidity reading event
"""

import time
import uuid

class Event:
    def __init__(self, humidity, temperature):
        self.event_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.humidity = humidity
        self.temperature = temperature
