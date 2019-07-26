"""
device.py

Device object;
- handles reading/writing of the device info file.
- handles setting up of sensor object
- handles recording of event objects into cache
"""
from lib.dht import DHT
from lib.lru_cache import LRUCache, calculate_cache_size
import src.event as event
from src.device_info import DeviceInfo
from src.device_info import generate_device_info_file, write_device_info_file, reset_device_info
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
            info = DeviceInfo(generate_initial_values=True)
            outfile.write(info.to_json())
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
        # define class properties
        self.device_info = None
        self.init_device_info()
        self.dht_sensor = DHT(Pin('P11', mode=Pin.OPEN_DRAIN), 1)
        self.events = LRUCache(calculate_cache_size(duration, interval))
        self.bluetooth_server = BluetoothServer(
            self.device_info.get_bluetooth_ids(),
            self.device_info.client_ids)

    def init_device_info(self):
        """
        init_device_info
        Reads device info if it exists.  Creates a new device info file otherwise.
        """
        if not does_file_exist(DEVICE_INFO_PATH):
            generate_device_info_file()

        self.read_device_info()

    def read_device_info(self):
        """
        read_device_info
        Reads the device info JSON file, parses it, and assigns data to device object
        """
        try:
            with uio.open(DEVICE_INFO_PATH, mode='r') as infile:
                device_data = ujson.loads(infile.read())
                self.device_info = DeviceInfo(device_data)
            infile.close()
        except OSError as err:
            print("Could not open ", DEVICE_INFO_PATH, err)

    def update_device_info(self):
        """
        update_device_info
        Writes updates to the device info file.
        """
        write_device_info_file(self.device_info)

    def reset_device_info(self):
        """
        reset_device_info
        Removes the existing device info file, and creates a new one
        """
        reset_device_info()
        self.read_device_info()

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
