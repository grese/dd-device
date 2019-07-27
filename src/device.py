"""
device.py

Contains the Device class. Used for interacting with device & managing data.
"""
from lib.dht import DHT
from lib.lru_cache import LRUCache, calculate_cache_size
import src.event as event
from src.device_info import generate_device_info_file, write_device_info_file
from src.device_info import reset_device_info, read_device_info_file, does_device_info_file_exist
from src.bluetooth import BluetoothServer
# MicroPython libraries:
from machine import Pin # pylint: disable=F0401

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
            bluetooth_ids=self.device_info.get_bluetooth_ids(),
            client_ids=self.device_info.client_ids,
            on_client_paired=self.__on_client_paired,
            on_client_unpaired=self.__on_client_unpaired)

    def init_device_info(self):
        """
        init_device_info
        Reads device info if it exists.  Creates a new device info file otherwise.
        """
        if not does_device_info_file_exist():
            generate_device_info_file()

        self.read_device_info()

    def read_device_info(self):
        """
        read_device_info
        Reads the device device info from file, and assigns the object to this class.
        """
        device_info = read_device_info_file()
        self.device_info = device_info

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

    def __on_client_paired(self, client_id):
        """
        __on_client_paired
        Triggered by BluetoothServer when a new client has paired.
        """
        if not client_id in self.device_info.client_ids:
            self.device_info.client_ids.add(client_id)
            self.update_device_info()
            self.bluetooth_server.update_client_ids(self.device_info.client_ids)

    def __on_client_unpaired(self, client_id):
        """
        __on_client_unpaired
        Triggered by BluetoothServer when a device has unpaired.
        """
        if client_id in self.device_info.client_ids:
            self.device_info.client_ids.discard(client_id)
            self.update_device_info()
            self.bluetooth_server.update_client_ids(self.device_info.client_ids)
