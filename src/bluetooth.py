
"""
bluetooth.py

Bluetooth connection, services, and client management
"""

from network import Bluetooth # pylint: disable=F0401

BT_ADV_PREFIX = 'dd-device-'
BT_MANUFACTURER_NAME = 'diaper-detective'
BT_DEVICE_VERSION = 'v0.0.1'

class BluetoothServer: # pylint: disable=C1001,R0903,R0902
    """
    BluetoothServer
    Advertises bluetooth services, handles connection and clients
    """
    def __init__(self, # pylint: disable=W0102
                 bluetooth_ids={},
                 client_ids=set(),
                 on_client_paired=None,
                 on_client_unpaired=None):
        # Read bluetooth IDs:
        self.__bt_id = bluetooth_ids.get('bt_id')
        self.__bt_pair_svc_id = bluetooth_ids.get('bt_pair_svc_id')
        self.__bt_sync_svc_id = bluetooth_ids.get('bt_sync_svc_id')
        self.__bt_pair_add_char_id = bluetooth_ids.get('bt_pair_add_char_id')
        self.__bt_pair_remove_char_id = bluetooth_ids.get('bt_pair_remove_char_id')
        self.__bt_sync_data_char_id = bluetooth_ids.get('bt_sync_data_char_id')
        self.__on_client_paired = on_client_paired
        self.__on_client_unpaired = on_client_unpaired
        # Save currently paired clients
        self.client_ids = client_ids
        # Setup bluetooth & configure advertisement.
        self.bluetooth = Bluetooth()
        self.bluetooth.set_advertisement(
            name=BT_ADV_PREFIX + str(self.__bt_id),
            service_uuid=self.__bt_id,
            manufacturer_data=BT_MANUFACTURER_NAME,
            service_data=BT_DEVICE_VERSION)
        # Create services:
        pair_service = self.bluetooth.service(uuid=self.__bt_pair_svc_id)
        sync_service = self.bluetooth.service(uuid=self.__bt_sync_svc_id)
        # Create characteristics for services:
        pair_add = pair_service.characteristic(
            uuid=self.__bt_pair_add_char_id,
            properties=Bluetooth.PROP_WRITE,
            value=None)
        pair_remove = pair_service.characteristic(
            uuid=self.__bt_pair_remove_char_id,
            properties=Bluetooth.PROP_WRITE,
            value=None)
        sync_data = sync_service.characteristic(
            uuid=self.__bt_sync_data_char_id,
            properties=Bluetooth.PROP_READ,
            value=None)
        # Add callbacks:
        self.bluetooth.callback(
            trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED,
            handler=self.__on_connection_status_changed)
        pair_add.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_pair_add,
            arg=None)
        pair_remove.callback(
            trigger=Bluetooth.CHAR_WRITE_EVENT,
            handler=self.__on_pair_remove,
            arg=None)
        sync_data.callback(
            trigger=Bluetooth.CHAR_READ_EVENT,
            handler=self.__on_sync_data,
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

    def __on_pair_add(self, ch): # pylint: disable=R0201,C0103
        """
        __on_pair_add
        Triggered from the pair-add characteristic.
        Expected data is the unique "client id" from the app.
        """
        client_id = ch.value().decode()
        self.__on_client_paired(client_id)
        print("pair_add: ", client_id)

    def __on_pair_remove(self, ch): # pylint: disable=R0201,C0103
        client_id = ch.value().decode()
        self.__on_client_unpaired(client_id)
        print("pair_remove: ", client_id)

    def __on_sync_data(self, ch): # pylint: disable=R0201,C0103
        print("sync_data: ", ch)
