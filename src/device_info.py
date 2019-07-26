
"""
device_info.py
"""

import os
import time
from lib.uuid import uuid4_str, bt_uuid
import ujson # pylint: disable=F0401
import uio # pylint: disable=F0401

# Path to json file where device info is stored
DEVICE_INFO_PATH = '/flash/device-info.json'

# pylint: disable=C0325

class DeviceInfo: # pylint: disable=C1001,R0902
    """
    DeviceInfo
    represents persistent device info
    """
    def __init__(self, initial_values=None, generate_initial_values=False):
        if initial_values:
            self.device_id = initial_values.get('device_id') or ''
            self.last_reset_time = initial_values.get('last_reset_time') or ''
            self.client_ids = set(initial_values.get('client_ids') or [])
            self.bt_id = initial_values.get('bt_id') or ''
            self.bt_pair_svc_id = initial_values.get('bt_pair_svc_id') or ''
            self.bt_sync_svc_id = initial_values.get('bt_sync_svc_id') or ''
            self.bt_pair_add_char_id = initial_values.get('bt_pair_add_char_id') or ''
            self.bt_pair_remove_char_id = initial_values.get('bt_pair_remove_char_id') or ''
            self.bt_sync_data_char_id = initial_values.get('bt_sync_data_char_id') or ''

        if generate_initial_values:
            self.__generate_initial_values()

    def __generate_initial_values(self):
        """
        init_values
        initializes the device info object with fresh data.
        """
        self.device_id = uuid4_str()
        self.last_reset_time = time.time()
        self.client_ids = set()
        self.bt_id = bt_uuid()
        self.bt_pair_svc_id = bt_uuid()
        self.bt_sync_svc_id = bt_uuid()
        self.bt_pair_add_char_id = bt_uuid()
        self.bt_pair_remove_char_id = bt_uuid()
        self.bt_sync_data_char_id = bt_uuid()

    def get_bluetooth_ids(self):
        """
        get_bluetooth_ids
        returns all of the bluetooth related IDs in a dictionary
        """
        return {
            "bt_id": self.bt_id,
            "bt_sync_svc_id": self.bt_sync_svc_id,
            "bt_pair_svc_id": self.bt_pair_svc_id,
            "bt_pair_add_char_id": self.bt_pair_add_char_id,
            "bt_pair_remove_char_id": self.bt_pair_remove_char_id,
            "bt_sync_data_char_id": self.bt_sync_data_char_id
            }

    def to_json(self):
        """
        to_json
        returns a JSON representation
        """
        return ujson.dumps({
            "device_id": self.device_id,
            "last_reset_time": self.last_reset_time,
            "client_ids": list(self.client_ids or []),
            "bt_id": self.bt_id,
            "bt_sync_svc_id": self.bt_sync_svc_id,
            "bt_pair_svc_id": self.bt_pair_svc_id,
            "bt_pair_add_char_id": self.bt_pair_add_char_id,
            "bt_pair_remove_char_id": self.bt_pair_remove_char_id,
            "bt_sync_data_char_id": self.bt_sync_data_char_id
            })


def write_device_info_file(device_info):
    """
    update_device_info_file
    Writes device info to file
    """
    try:
        with uio.open(DEVICE_INFO_PATH, mode='w') as outfile:
            json_str = device_info.to_json()
            if len(json_str): # pylint: disable=C1801
                outfile.write(json_str)
        outfile.close()
    except ValueError as err:
        print('Error converting device info to JSON', err)
    except OSError as err:
        print('Could not write device info file', err)

def generate_device_info_file():
    """
    generate_device_info_file
    Creates a new device_info_file
    """
    write_device_info_file(DeviceInfo(generate_initial_values=True))

def reset_device_info():
    """
    reset_device_info
    Removes device info file and generates a new one.
    """
    os.remove(DEVICE_INFO_PATH)
    generate_device_info_file()
