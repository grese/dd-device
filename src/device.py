"""
device.py

Contains the Device class. Used for interacting with device & managing data.
"""
from lib.dht import DHT
from src.sensor_data import SensorData
from src.sensor_cache import SensorCache, calculate_cache_size
from src.event_cache import EventCache
from src.event import Event, EventType
from src.device_info import generate_device_info_file, write_device_info_file
from src.device_info import reset_device_info, read_device_info_file, does_device_info_file_exist
from src.bluetooth import BluetoothServer
# MicroPython libraries:
import ujson  # pylint: disable=F0401
from machine import Pin # pylint: disable=F0401

HUMIDITY_THRESHOLD = 90
HUMIDITY_DRY_THRESHOLD = 80
MIN_TIME_BETWEEN_EVENTS = 60 # 1 minute.

class Device: # pylint: disable=C1001
    """
    Device
    Represents the device itself.  Exposes methods for interacting with sensors,
    connecting bluetooth, etc.
    """
    def __init__(self, duration, interval, num_events):
        # define class properties
        self.device_info = None
        self.init_device_info()
        self.dht_sensor = DHT(Pin('P11', mode=Pin.OPEN_DRAIN), 1)
        self.sensor_data = SensorCache(calculate_cache_size(duration, interval))
        self.interval = interval
        self.events = EventCache(num_events)
        self.bluetooth_server = BluetoothServer(
            device_id=self.device_info.device_id,
            bluetooth_ids=self.device_info.get_bluetooth_ids(),
            client_ids=self.device_info.client_ids,
            on_client_paired=self.__on_client_paired,
            on_client_unpaired=self.__on_client_unpaired,
            get_next_data_item=self.get_next_data_json,
            get_next_event_item=self.get_next_event_json,
            clear_event=self.clear_event)

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
            self.sensor_data.push(data)
            data.log_data() # log data to console
        else:
            print('Invalid sensor data.', dht_result)

    def check_for_event(self):
        """
        check_for_event
        Analyzes sensor data, and creates a new Event object if necessary

        Event "one" Conditions:
        - humidity must have been increasing for specified period of time
        - humidity value must exceed humidity threshold
        - an event must not have been fired within specified time.

        Event "changed" conditions
        - humidity less than the "dry" humidity threshold.
        - humidity must have been decreasing for specified period of time.
        - must have been long enough since last event was fired.
        """
        last_data = self.sensor_data.peek()
        last_event = self.events.peek()
        # dirty event conditions:
        humidity_exceeds_threshold = last_data.humidity >= HUMIDITY_THRESHOLD
        is_humidity_increasing = self.sensor_data.is_humidity_increasing()
        long_enough_since_last_event = True if not last_event else (last_data.timestamp - last_event.timestamp > MIN_TIME_BETWEEN_EVENTS) # pylint: disable=C0301
        # change event conditions:
        is_humidity_decreasing = self.sensor_data.is_humidity_decreasing()
        humidity_dry_enough = last_data.humidity <= HUMIDITY_DRY_THRESHOLD

        event = None
        if is_humidity_increasing and long_enough_since_last_event and humidity_exceeds_threshold:
            event = Event()
        elif is_humidity_decreasing and long_enough_since_last_event and humidity_dry_enough:
            event = Event(EventType.changed)

        if event:
            self.events.push(event)
            self.bluetooth_server.send_event_notification(event)

    def get_next_data_json(self):
        """
        get_next_data_json
        Removes oldest data point from cache, and returns as JSON string.
        """
        item = self.sensor_data.deque()
        items_left = self.sensor_data.length()
        result = {"remaining": items_left}
        if item:
            result["data"] = item.to_dict()
        return ujson.dumps(result)

    def get_next_event_json(self):
        """
        get_next_event_json
        Removes oldest event from cache, and returns as JSON string.
        """
        event = self.events.deque()
        events_left = self.events.length()
        result = {"remaining": events_left}
        if event:
            result["event"] = event.to_dict()
        return ujson.dumps(result)

    def clear_event(self, e_id):
        """
        clear_event
        Removes event from cache
        """
        # Find & remove the existing event if it exists.
        event = self.events.find_by_id(e_id)
        if event:
            self.events.remove_event(event)
        # Generate the 'change' event, and pass to client.
        new_event = Event(EventType.changed)
        self.events.push(new_event)
        self.bluetooth_server.send_event_notification(event)

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
