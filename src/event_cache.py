
"""
event_cache.py
A cache that holds sensor data until it is synced.
"""

from src.event import EventType

class EventCache: # pylint: disable=C1001
    """
    EventCache
    Cache for events.  Works like a stack.
    """
    def __init__(self, max_size):
        self.__max_size = max_size
        self.__cache = []

    def has_unhandled_events(self):
        """
        has_unhandled_events
        Returns true if there are events with type one or two.
        """
        for evt in self.__cache:
            if evt.event_type != EventType.changed:
                return True
        return False

    def remove_event(self, event):
        """
        remove_event
        removes event from cache
        """
        self.__cache.remove(event)

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
