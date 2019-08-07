
"""
event_cache.py
A cache that holds sensor data until it is synced.
"""
import utime # pylint: disable=E0401
from src.event import EventType

class EventCache: # pylint: disable=C1001
    """
    EventCache
    Cache for events.  Works like a stack.
    """
    def __init__(self, max_size):
        self.__max_size = max_size
        self.__cache = []
        self.__last_dirty_timestamp = 0
        self.__last_clear_timestamp = 0

    def time_since_last_dirty_event(self):
        """
        time_since_last_dirty_event
        Returns time since last dirty event
        """
        return utime.time() - self.__last_dirty_timestamp

    def time_since_last_clear_event(self):
        """
        time_since_last_clear_event
        Returns time since last dirty event
        """
        return utime.time() - self.__last_clear_timestamp

    def has_unhandled_events(self):
        """
        has_unhandled_events
        Returns true if there are events with type one or two.
        """
        for evt in self.__cache:
            if evt.event_type != EventType.changed:
                return True
        return False

    def remove_event(self, event_id):
        """
        remove_event
        removes event from cache
        """
        found_event = self.find_by_id(event_id)
        if found_event:
            self.__cache.remove(found_event)
        else:
            print("Cannot remove event {}. Does not exist.".format(event_id)) # pylint: disable=C0325

    def find_by_id(self, event_id):
        """
        find_by_id
        finds an event by id
        """
        for e in self.__cache: # pylint: disable=C0103
            if e.event_id == event_id:
                return e
        return None

    def length(self):
        """
        length
        returns number of items in cache
        """
        return len(self.__cache)

    def push(self, event):
        """
        push
        adds an item to the cache
        """
        if len(self.__cache) == self.__max_size:
            self.deque()
        self.__cache.append(event)

        if event.event_type == EventType.changed:
            self.__last_clear_timestamp = event.timestamp
        else:
            self.__last_dirty_timestamp = event.timestamp

    def peek(self):
        """
        peek
        returns the top of the stack without removing it.
        """
        if self.__cache:
            return self.__cache[-1]
        return None

    def deque(self):
        """
        deque
        removes and returns the first item from the cache
        """
        if self.__cache:
            return self.__cache.pop(0)
        return None
