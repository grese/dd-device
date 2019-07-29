"""
device.py

Contains the Device class. Used for interacting with device & managing data.
"""
from lib.dht import DHT
from lib.lru_cache import LRUCache, calculate_cache_size
from src.sensor_data import SensorData
from src.event import Event
from src.device_info import generate_device_info_file, write_device_info_file
from src.device_info import reset_device_info, read_device_info_file, does_device_info_file_exist
from src.bluetooth import BluetoothServer
# MicroPython libraries:
import ujson  # pylint: disable=F0401
from machine import Pin # pylint: disable=F0401

HUMIDITY_THRESHOLD = 90.0

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
        self.sensor_data = LRUCache(calculate_cache_size(duration, interval))
        self.events = []
        self.bluetooth_server = BluetoothServer(
            device_id=self.device_info.device_id,
            bluetooth_ids=self.device_info.get_bluetooth_ids(),
            client_ids=self.device_info.client_ids,
            on_client_paired=self.__on_client_paired,
            on_client_unpaired=self.__on_client_unpaired,
            get_sync_data=self.get_sync_data_json)

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

    def read_sensor_data(self):
        """
        read_sensor_data
        Reads sensor data, and adds an SensorData object to the cache
        """
        dht_result = self.dht_sensor.read()
        if dht_result.is_valid():
            data = SensorData(dht_result.humidity, dht_result.temperature)
            self.sensor_data.set(data.data_id, data)
            data.log_data() # log data to console
        else:
            print('Invalid sensor data.', dht_result)

    def check_for_event(self):
        """
        check_for_event
        Analyzes sensor data, and creates a new Event object if necessary
        """
        last_data = None
        for key in self.sensor_data.cache:
            item = self.sensor_data.cache[key]
            if not last_data or item.timestamp > last_data.timestamp:
                last_data = item
        if last_data and last_data.humidity >= HUMIDITY_THRESHOLD:
            event = Event()
            self.events.append(event)
            print("Event detected! ", last_data.humidity)

    def get_sync_data_json(self):
        """
        get_sync_data_json
        Returns sensor data and events as stringified JSON
        """
        data = []
        for key in self.sensor_data.cache:
            item = self.sensor_data.cache[key]
            data.append(item.to_dict())
        events = []
        for event in self.events:
            events.append(event.to_dict())
        return ujson.dumps({"sensor_data": data, "events": events})

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
