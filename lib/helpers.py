
import time

def current_timestamp():
    return "%04u-%02u-%02uT%02u:%02u:%02u" % time.localtime(t)[0:6]
