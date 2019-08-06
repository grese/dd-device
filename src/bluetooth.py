
"""
bluetooth.py

Bluetooth connection, services, and client management
"""
from network import Bluetooth # pylint: disable=F0401
from lib.uuid import uuid2bytes
from lib.helpers import set_current_time, current_timestamp

BT_ADV_PREFIX = 'dd-device-'
BT_MANUFACTURER_NAME = 'diaper-detective'
BT_DEVICE_VERSION = 'v0.0.1'
EVENT_CLEAR_PREFIX = 'event_cleared='
TIME_SETUP_PREFIX = 'setup_time='

class BluetoothServer: # pylint: disable=C1001,R0903,R0902
    """
    BluetoothServer
    Advertises bluetooth services, handles connection and clients
    """
    def __init__(self, # pylint: disable=W0102,R0913,R0914
                 device_id='',
                 bluetooth_ids={},
                 client_ids=set(),
                 on_client_paired=None,
                 on_client_unpaired=None,
                 get_next_data_item=None,
                 get_next_event_item=None,
                 clear_event=None):
        # Read bluetooth IDs:
        self.__device_id = device_id
        self.__bt_id = bluetooth_ids.get('bt_id')
        self.__bt_setup_svc_id = bluetooth_ids.get('bt_setup_svc_id')
        self.__bt_pair_svc_id = bluetooth_ids.get('bt_pair_svc_id')
        self.__bt_unpair_svc_id = bluetooth_ids.get('bt_unpair_svc_id')
        self.__bt_data_svc_id = bluetooth_ids.get('bt_data_svc_id')
        self.__bt_event_svc_id = bluetooth_ids.get('bt_event_svc_id')
        self.__bt_event_notif_svc_id = bluetooth_ids.get('bt_event_notif_svc_id')
        self.__bt_event_clear_svc_id = bluetooth_ids.get('bt_event_clear_svc_id')
        self.__bt_setup_char_id = bluetooth_ids.get('bt_setup_char_id')
        self.__bt_pair_char_id = bluetooth_ids.get('bt_pair_char_id')
        self.__bt_unpair_char_id = bluetooth_ids.get('bt_unpair_char_id')
        self.__bt_data_char_id = bluetooth_ids.get('bt_data_char_id')
        self.__bt_event_char_id = bluetooth_ids.get('bt_event_char_id')
        self.__bt_event_notif_char_id = bluetooth_ids.get('bt_event_notif_char_id')
        self.__bt_event_clear_char_id = bluetooth_ids.get('bt_event_clear_char_id')
        self.__on_client_paired = on_client_paired
        self.__on_client_unpaired = on_client_unpaired
        self.__get_next_data_item = get_next_data_item
        self.__get_next_event_item = get_next_event_item
        self.__clear_event = clear_event
        # Save currently paired clients
        self.client_ids = client_ids
        # Setup bluetooth & configure advertisement.
        self.bluetooth = Bluetooth()
        self.bluetooth.set_advertisement(
            name=BT_ADV_PREFIX + self.__device_id,
            service_uuid=uuid2bytes(self.__bt_id),
            manufacturer_data=BT_MANUFACTURER_NAME,
            service_data=BT_DEVICE_VERSION)
        # Create services:
        setup_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_setup_svc_id),
            isprimary=True)
        pair_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_pair_svc_id),
            isprimary=True)
        unpair_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_unpair_svc_id),
            isprimary=True)
        data_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_data_svc_id),
            isprimary=True)
        event_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_event_svc_id),
            isprimary=True,
            nbr_chars=2)
        event_notif_service = self.bluetooth.service(
            uuid=uuid2bytes(self.__bt_event_notif_svc_id),
            isprimary=True)
        # event_clear_service = self.bluetooth.service(
        #     uuid=uuid2bytes(self.__bt_event_clear_svc_id),
        #     isprimary=True)

        # Create characteristics for services:
        self.__setup_char = setup_service.characteristic(
            uuid=uuid2bytes(self.__bt_setup_char_id),
            properties=Bluetooth.PROP_WRITE,
            value=None)
        self.__pair_char = pair_service.characteristic(
            uuid=uuid2bytes(self.__bt_pair_char_id),
            properties=Bluetooth.PROP_WRITE,
            value=None)
        self.__unpair_char = unpair_service.characteristic(
            uuid=uuid2bytes(self.__bt_unpair_char_id),
            properties=Bluetooth.PROP_WRITE,
            value=None)
        self.__data_char = data_service.characteristic(
            uuid=uuid2bytes(self.__bt_data_char_id),
            properties=Bluetooth.PROP_READ,
            value=None)
        self.__event_char = event_service.characteristic(
            uuid=uuid2bytes(self.__bt_event_char_id),
            properties=Bluetooth.PROP_READ, # pylint: disable=C0301
            value=None)
        self.__event_notif_char = event_notif_service.characteristic(
            uuid=uuid2bytes(self.__bt_event_notif_char_id),
            properties=Bluetooth.PROP_NOTIFY | Bluetooth.PROP_INDICATE,
            value=None)
        self.__event_clear_char = event_service.characteristic(
            uuid=uuid2bytes(self.__bt_event_clear_char_id),
            properties=Bluetooth.PROP_WRITE,
            value=None)

        # Add callbacks:
        self.bluetooth.callback(
            trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED,
            handler=self.__on_connection_status_changed)
        self.__setup_char.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_setup_write,
            arg=None)
        self.__pair_char.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_pair_write,
            arg=None)
        self.__unpair_char.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_unpair_write,
            arg=None)
        self.__data_char.callback(
            trigger=Bluetooth.CHAR_READ_EVENT,
            handler=self.__on_data_read,
            arg=None)
        self.__event_char.callback(
            trigger=Bluetooth.CHAR_READ_EVENT,
            handler=self.__on_event_read,
            arg=None)
        self.__event_clear_char.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_event_clear,
            arg=None)
        # Start advertising:
        self.bluetooth.advertise(True)

    def update_client_ids(self, client_ids):
        """
        set_client_ids
        Update the client_ids
        """
        self.client_ids = client_ids

    def __on_connection_status_changed(self, bt_o):
        events = bt_o.events()
        if events & Bluetooth.CLIENT_CONNECTED:
            self.__on_client_connected(bt_o)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            self.__on_client_disconnected(bt_o)

    def __on_client_connected(self, bt_o): # pylint: disable=R0201
        adv = bt_o.get_adv()
        print('Client connected: ', adv)

    def __on_client_disconnected(self, bt_o): # pylint: disable=R0201
        adv = bt_o.get_adv()
        print('Client disconnected: ', adv)

    def __on_setup_write(self, ch):# pylint: disable=R0201,C0103
        """
        __on_setup_write
        Setup device
        """
        data = ch.value().decode()
        print("setup_write: ", data)
        if TIME_SETUP_PREFIX in data:
            time_vals = data.replace(TIME_SETUP_PREFIX, "", 1)
            time_vals = [int(x) for x in time_vals.split(",")]
            set_current_time((time_vals[0],
                              time_vals[1],
                              time_vals[2],
                              time_vals[3],
                              time_vals[4],
                              time_vals[5]))
            print("Current timestamp: ", current_timestamp())

    def __on_pair_write(self, ch): # pylint: disable=C0103
        """
        __on_pair_write
        Triggered from the pair-write characteristic.
        Expected data is the unique "client id" from the app.
        """
        client_id = ch.value().decode()
        self.__on_client_paired(client_id)
        print("pair_write: ", client_id)

    def __on_unpair_write(self, ch): # pylint: disable=C0103
        client_id = ch.value().decode()
        self.__on_client_unpaired(client_id)
        print("unpair_write: ", client_id)

    def __on_data_read(self, ch): # pylint: disable=C0103
        """
        __on_data_read
        Triggered from the data characteristic.
        """
        data = self.__get_next_data_item()
        ch.value(data)
        print("data_read: ", data)

    def __on_event_read(self, ch): # pylint: disable=C0103
        """
        __on_event_read
        Triggered from the event characteristic.
        """
        data = self.__get_next_event_item()
        ch.value(data)
        print("event_read: ", data)

    def __on_event_clear(self, ch): # pylint: disable=C0103
        """
        __on_event_clear
        Triggered from event_clear characteristic
        """
        data = ch.value().decode()
        if EVENT_CLEAR_PREFIX in data:
            e_id = data.replace(EVENT_CLEAR_PREFIX, "", 1)
            self.__clear_event(e_id)

    def send_event_notification(self, event):
        """
        send_event_notification
        """
        print("Notifying client of event: ", event.event_id)
        self.__event_notif_char.value("new_event=" + event.event_id)
