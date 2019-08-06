
"""
sensor_cache.py
A cache that holds sensor data until it is synced.
"""

HUMIDITY_SWING_SIZE = 3 # number of items to consider delta increasing or decreasing
MIN_HUMIDITY_CHANGE = 10

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

    def peek(self, index=-1):
        """
        peek
        returns the top of the stack without removing it.
        """
        if self.__cache:
            return self.__cache[index]
        return None

    def peek_n(self, n=1): # pylint: disable=C0103
        """
        peek_n
        returns n items from top of stack without removing.
        """
        if self.__cache:
            return self.__cache[-1 * n:]
        return []

    def pop(self, index=None):
        """
        deque
        removes and returns the top of the stack (or the item at specified index)
        """
        if self.__cache:
            return self.__cache.pop(index)
        return None

    def deque(self):
        """
        deque
        removes and returns the first item from the cache
        """
        return self.pop(0)

    def is_humidity_decreasing(self, swing_size=HUMIDITY_SWING_SIZE):
        """
        is_humidity_decreasing
        returns true if the humidity is decreasing
        """
        if self.length() < swing_size:
            return False
        items = self.peek_n(swing_size)
        prev_item = items.pop(0)
        for item in items:
            if prev_item.humidity < item.humidity:
                return False
            prev_item = item
        return items[0].humidity - items[-1].humidity > MIN_HUMIDITY_CHANGE

    def is_humidity_increasing(self, swing_size=HUMIDITY_SWING_SIZE):
        """
        is_humidity_increasing
        returns true if the humidity is increasing
        """
        if self.length() < swing_size:
            return False
        items = self.peek_n(swing_size)
        prev_item = items.pop(0)
        for item in items:
            if prev_item.humidity > item.humidity:
                return False
            prev_item = item
        # return items[-1].humidity - items[0].humidity > MIN_HUMIDITY_CHANGE
        return True

def calculate_cache_size(duration, interval):
    """
    calculate_cache_size
    Calculates the necessary size for cache based on interval and number of days
    duration = number of days
    interval = number of seconds between updates.
    """
    return (60 / interval) * 60 * 24 * duration
