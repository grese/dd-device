"""
device.py

Device object;
- handles reading/writing of the device info file.
- handles setting up of sensor object
- handles recording of event objects into cache
"""
import os
import time
from lib.dht import DHT
from lib.lru_cache import LRUCache, calculate_cache_size
import lib.uuid as uuid
import src.event as event
from src.bluetooth import BluetoothServer
# MicroPython libraries:
import ujson # pylint: disable=F0401
import uio   # pylint: disable=F0401
from machine import Pin # pylint: disable=F0401

# Path to json file where device info is stored
DEVICE_INFO_PATH = '/flash/device-info.json'

def create_device_info_file():
    """
    create_device_info_file
    Creates the device info json file with a fresh deviceID
    """
    device_uuid = str(uuid.uuid4())
    last_reset_time = time.time()
    try:
        with uio.open(DEVICE_INFO_PATH, mode='w') as outfile:
            data = {
                "device_id": device_uuid,
                "last_reset_time": last_reset_time,
                "user_id": ""
            }
            outfile.write(ujson.dumps(data))
        outfile.close()
    except OSError as err:
        print("Could not create device info file: ", err)

def does_file_exist(filename):
    """
    does_file_exist
    Returns true if the given filename exists, false otherwise.
    """
    exists = False
    try:
        with uio.open(filename, mode='r'):
            exists = True
    except OSError:
        pass
    return exists

class Device: # pylint: disable=C1001
    """
    Device
    Represents the device itself.  Exposes methods for interacting with sensors,
    connecting bluetooth, etc.
    """
    def __init__(self, duration, interval):
        self.device_id = None
        self.last_reset_time = 0
        self.user_id = None
        self.init_device_info()
        self.dht_sensor = DHT(Pin('P11', mode=Pin.OPEN_DRAIN), 1)
        self.events = LRUCache(calculate_cache_size(duration, interval))
        self.bluetooth_server = BluetoothServer()

    def init_device_info(self):
        """
        init_device_info
        Reads device info if it exists.  Creates a new device info file otherwise.
        """
        if not does_file_exist(DEVICE_INFO_PATH):
            create_device_info_file()

        self.read_device_info()

    def read_device_info(self):
        """
        read_device_info
        Reads the device info JSON file, parses it, and assigns data to device object
        """
        try:
            with uio.open(DEVICE_INFO_PATH, mode='r') as infile:
                device_data = ujson.loads(infile.read())
                self.device_id = device_data['device_id']
                self.last_reset_time = device_data['last_reset_time']
                self.user_id = device_data['user_id']
            infile.close()
        except OSError as err:
            print("Could not open ", DEVICE_INFO_PATH, err)

    def reset_device_info(self):
        """
        reset_device_info
        Removes the existing device info file, and creates a new one
        """
        os.remove(DEVICE_INFO_PATH)
        self.init_device_info()

    def create_event(self):
        """
        create_event
        Reads sensor data, and adds an event object to the cache
        """
        dht_result = self.dht_sensor.read()
        if dht_result.is_valid():
            print('Creating event.') # pylint: disable=C0325
            new_event = event.Event(dht_result.humidity, dht_result.temperature)
            self.events.set(new_event.event_id, new_event)
            new_event.log() # log event data to console
        else:
            print('Invalid sensor data.', dht_result)
