
"""
sensor_cache.py
A cache that holds sensor data until it is synced.
"""

class SensorCache: # pylint: disable=C1001
    """
    SensorCache
    Cache for sensor data.  Works like a stack.
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

    def push(self, sensor_data):
        """
        push
        adds an item to the cache
        """
        if len(self.__cache) == self.__max_size:
            self.deque()
        self.__cache.append(sensor_data)

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

def calculate_cache_size(duration, interval):
    """
    calculate_cache_size
    Calculates the necessary size for cache based on interval and number of days
    duration = number of days
    interval = number of seconds between updates.
    """
    return (60 / interval) * 60 * 24 * duration
