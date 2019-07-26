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
from lib.uuid import uuid4_str, bt_uuid
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
    try:
        with uio.open(DEVICE_INFO_PATH, mode='w') as outfile:
            data = {
                "device_id": uuid4_str(),
                "last_reset_time": time.time(),
                "user_id": "",
                "client_ids": [],
                "bt_id": bt_uuid(),
                "bt_sync_svc_id": bt_uuid(),
                "bt_pair_svc_id": bt_uuid(),
                "bt_pair_add_char_id": bt_uuid(),
                "bt_pair_remove_char_id": bt_uuid(),
                "bt_sync_data_char_id": bt_uuid()
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
        self.client_ids = []
        self.bluetooth_ids = {}
        self.init_device_info()
        self.dht_sensor = DHT(Pin('P11', mode=Pin.OPEN_DRAIN), 1)
        self.events = LRUCache(calculate_cache_size(duration, interval))
        self.bluetooth_server = BluetoothServer(self.bluetooth_ids, self.client_ids)

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
                self.device_id = device_data.get('device_id')
                self.last_reset_time = device_data.get('last_reset_time')
                self.user_id = device_data.get('user_id')
                self.client_ids = device_data.get('client_ids')
                self.bluetooth_ids = {
                    "bt_id": device_data.get('bt_id') or '',
                    "bt_pair_svc_id": device_data.get('bt_pair_svc_id') or '',
                    "bt_sync_svc_id": device_data.get('bt_sync_svc_id') or '',
                    "bt_pair_add_char_id": device_data.get('bt_pair_add_char_id') or '',
                    "bt_pair_remove_char_id": device_data.get('bt_pair_remove_char_id') or '',
                    "bt_sync_data_char_id": device_data.get('bt_sync_data_char_id') or ''
                }
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
