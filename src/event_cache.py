
"""
event_cache.py
A cache that holds sensor data until it is synced.
"""

class EventCache: # pylint: disable=C1001
    """
    EventCache
    Cache for events.  Works like a stack.
    """
    def __init__(self, max_size):
        self.__max_size = max_size
        self.__cache = []

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
