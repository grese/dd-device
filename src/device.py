"""
device.py

Device object;
- handles reading/writing of the device info file.
- handles setting up of sensor object
- handles recording of event objects into cache
"""

import os
import time
import ujson
import uio
from machine import Pin
from lib.dht import DHT
import lib.lru_cache as lru_cache
import lib.uuid as uuid
import src.event as event

# Path to json file where device info is stored
device_info_path = '/flash/device-info.json'

# Event cache size:
cache_size = 40320 # every 30 seconds for 1 week ((60 / 15) * 60 * 24 * 7)

def create_device_info_file():
    device_uuid = str(uuid.uuid4())
    last_reset_time = time.time()
    try:
        f = uio.open(device_info_path, mode='w')
        data = {
            "device_id": device_uuid,
            "last_reset_time": last_reset_time,
            "user_id": ""
        }
        f.write(ujson.dumps(data))
        f.close()
    except OSError as e:
        print("Could not create device info file: ", e)

def does_file_exist(filename):
    exists = False
    try:
        with uio.open(filename, 'r') as fh:
            exists = True
    except:
        pass
    return exists

class Device:
    def __init__(self):
        self.init_device_info()
        self.dht_sensor = DHT(Pin('P11', mode=Pin.OPEN_DRAIN),1)
        self.events = lru_cache.LRUCache(cache_size)

    def init_device_info(self):
        if not does_file_exist(device_info_path):
            create_device_info_file()

        self.read_device_info()

    def read_device_info(self):
        try:
            with uio.open(device_info_path, 'r') as f:
                device_data = ujson.loads(f.read())
                self.device_id = device_data['device_id']
                self.last_reset_time = device_data['last_reset_time']
                self.user_id = device_data['user_id']
            f.close()
        except OSError as e:
            print("Could not open ", device_info_path, e)

    def reset_device_info(self):
        os.remove(device_info_path)
        self.init_device_info()

    def create_event(self):
        dht_result = self.dht_sensor.read()
        if dht_result.is_valid():
            print('Creating event.')
            new_event = event.Event(dht_result.humidity, dht_result.temperature)
            self.events.set(new_event.event_id, new_event)
            self.log_event(new_event)
        else:
            print('Invalid sensor data.', dht_result)

    def log_event(self, event):
        print('Humidity: ', event.humidity)
        print('Temperature: ', event.temperature)
        print()
