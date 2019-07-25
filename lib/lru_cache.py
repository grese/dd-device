"""
LRUCache

A simple Least recently used cache
======================
https://www.kunxi.org/2014/05/lru-cache-in-python/
"""

# pylint: disable=C0103
class LRUCache: # pylint: disable=C1001
    """
    LRUCache
    least recently used cache
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.tm = 0
        self.cache = {}
        self.lru = {}

    def get(self, key):
        """
        get
        returns the cache item for a given key
        """
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            return self.cache[key]
        return -1

    def set(self, key, value):
        """
        set
        sets the key equal to the value in the cache
        """
        if len(self.cache) >= self.capacity:
            # find the LRU entry
            old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)
        self.cache[key] = value
        self.lru[key] = self.tm
        self.tm += 1
