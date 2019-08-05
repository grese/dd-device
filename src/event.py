
"""
Event
Class representing humidity reading event
"""

import time
import uuid
from lib.helpers import current_timestamp

class EventType: # pylint: disable=C1001,W0232,R0903
    """
    EventType
    event types
    """
    one = 1
    two = 2
    changed = 3

class Event: # pylint: disable=C1001, R0903
    """
    Event
    Represents an event derived from changes in humidity/temperature
    """
    def __init__(self, event_type=EventType.one):
        self.event_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.event_type = 1
        self.timestamp = current_timestamp()
        self.event_type = event_type

    def log(self):
        """
        log_event
        Prints an event's data to the console
        """
        print('Event occurred ', self.event_id, self.timestamp)
        print()

    def to_dict(self):
        """
        to_json
        returns event data as dictionary
        """
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type
            }
