
"""
device_info.py
"""

import os
from lib.helpers import current_timestamp
import ujson # pylint: disable=F0401
import uio # pylint: disable=F0401

# Path to json file where device info is stored
DEVICE_INFO_PATH = '/flash/device-info.json'
# Hard-coded IDs (unique per device)
DEVICE_ID = '5d2e97cb6532994c'
BT_ID = '26130984-4221-4008-8402-01008040a050'
# IDs for bluetooth services & characteristics (same on every device)
BT_SETUP_SVC_ID = '5b2d96cb-6532-494c-a693-49249249a4d2'
BT_PAIR_SVC_ID = '0c060381-c0e0-4078-bcde-6fb7dbed763b'
BT_UNPAIR_SVC_ID = 'd66b351a-0d06-4341-a050-a854aa552a95'
BT_DATA_SVC_ID = '9dce6733-198c-46e3-b138-9cce67b3d96c'
BT_EVENT_SVC_ID = '48241209-0402-41c0-a070-389cce673399'
BT_EVENT_NOTIF_SVC_ID = '77e90f18-69ae-4283-bf53-f940e4588afa'
BT_EVENT_CLEAR_SVC_ID = '8b30ec19-6368-4920-939b-80c8cd24b3b0'
BT_PAIR_CHAR_ID = '369bcde6-73b9-4cae-97eb-753a9dcee773'
BT_UNPAIR_CHAR_ID = 'b95caed7-eb75-4a9d-8e67-b359acd6eb75'
BT_DATA_CHAR_ID = 'cae57239-9c4e-4793-89e4-72b9dc6e379b'
BT_EVENT_CHAR_ID = '6db65bad-d66b-45da-adf6-7bbd5eaf57ab'
BT_EVENT_NOTIF_CHAR_ID = 'a647940e-ebc1-4bd4-b273-a600929476cd'
BT_EVENT_CLEAR_CHAR_ID = 'ee7a4fc7-6305-48e1-92e9-7c1c9be13b63'
BT_SETUP_CHAR_ID = '2e97cbe5-f2f9-4c3e-9f0f-0783c1603018'

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
            self.bt_setup_svc_id = initial_values.get('bt_setup_svc_id') or ''
            self.bt_pair_svc_id = initial_values.get('bt_pair_svc_id') or ''
            self.bt_unpair_svc_id = initial_values.get('bt_unpair_svc_id') or ''
            self.bt_data_svc_id = initial_values.get('bt_data_svc_id') or ''
            self.bt_event_svc_id = initial_values.get('bt_event_svc_id') or ''
            self.bt_event_notif_svc_id = initial_values.get('bt_event_notif_svc_id') or ''
            self.bt_event_clear_svc_id = initial_values.get('bt_event_clear_svc_id') or ''
            self.bt_setup_char_id = initial_values.get('bt_setup_char_id') or ''
            self.bt_pair_char_id = initial_values.get('bt_pair_char_id') or ''
            self.bt_unpair_char_id = initial_values.get('bt_unpair_char_id') or ''
            self.bt_data_char_id = initial_values.get('bt_data_char_id') or ''
            self.bt_event_char_id = initial_values.get('bt_event_char_id') or ''
            self.bt_event_notif_char_id = initial_values.get('bt_event_notif_char_id') or ''
            self.bt_event_clear_char_id = initial_values.get('bt_event_clear_char_id') or ''

        if generate_initial_values:
            self.__generate_initial_values()

    def __generate_initial_values(self):
        """
        init_values
        initializes the device info object with fresh data.
        """
        self.device_id = DEVICE_ID
        self.last_reset_time = current_timestamp()
        self.client_ids = set()
        self.bt_id = BT_ID
        self.bt_setup_svc_id = BT_SETUP_SVC_ID
        self.bt_pair_svc_id = BT_PAIR_SVC_ID
        self.bt_unpair_svc_id = BT_UNPAIR_SVC_ID
        self.bt_data_svc_id = BT_DATA_SVC_ID
        self.bt_event_svc_id = BT_EVENT_SVC_ID
        self.bt_event_notif_svc_id = BT_EVENT_NOTIF_SVC_ID
        self.bt_event_clear_svc_id = BT_EVENT_CLEAR_SVC_ID
        self.bt_setup_char_id = BT_SETUP_CHAR_ID
        self.bt_pair_char_id = BT_PAIR_CHAR_ID
        self.bt_unpair_char_id = BT_UNPAIR_CHAR_ID
        self.bt_data_char_id = BT_DATA_CHAR_ID
        self.bt_event_char_id = BT_EVENT_CHAR_ID
        self.bt_event_notif_char_id = BT_EVENT_NOTIF_CHAR_ID
        self.bt_event_clear_char_id = BT_EVENT_CLEAR_CHAR_ID

    def get_bluetooth_ids(self):
        """
        get_bluetooth_ids
        returns all of the bluetooth related IDs in a dictionary
        """
        return {
            "bt_id": self.bt_id,
            "bt_setup_svc_id": self.bt_setup_svc_id,
            "bt_pair_svc_id": self.bt_pair_svc_id,
            "bt_unpair_svc_id": self.bt_unpair_svc_id,
            "bt_data_svc_id": self.bt_data_svc_id,
            "bt_event_svc_id": self.bt_event_svc_id,
            "bt_event_notif_svc_id": self.bt_event_notif_svc_id,
            "bt_event_clear_svc_id": self.bt_event_clear_svc_id,
            "bt_setup_char_id": self.bt_setup_char_id,
            "bt_pair_char_id": self.bt_pair_char_id,
            "bt_unpair_char_id": self.bt_unpair_char_id,
            "bt_data_char_id": self.bt_data_char_id,
            "bt_event_char_id": self.bt_event_char_id,
            "bt_event_notif_char_id": self.bt_event_notif_char_id,
            "bt_event_clear_char_id": self.bt_event_clear_char_id
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
            "bt_setup_svc_id": self.bt_setup_svc_id,
            "bt_pair_svc_id": self.bt_pair_svc_id,
            "bt_unpair_svc_id": self.bt_unpair_svc_id,
            "bt_data_svc_id": self.bt_data_svc_id,
            "bt_event_svc_id": self.bt_event_svc_id,
            "bt_event_notif_svc_id": self.bt_event_notif_svc_id,
            "bt_event_clear_svc_id": self.bt_event_clear_svc_id,
            "bt_setup_char_id": self.bt_setup_char_id,
            "bt_pair_char_id": self.bt_pair_char_id,
            "bt_unpair_char_id": self.bt_unpair_char_id,
            "bt_data_char_id": self.bt_data_char_id,
            "bt_event_char_id": self.bt_event_char_id,
            "bt_event_notif_char_id": self.bt_event_notif_char_id,
            "bt_event_clear_char_id": self.bt_event_clear_char_id
            })

# Functions:

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
    new_device_info = DeviceInfo(generate_initial_values=True)
    write_device_info_file(new_device_info)

def reset_device_info():
    """
    reset_device_info
    Removes device info file and generates a new one.
    """
    os.remove(DEVICE_INFO_PATH)
    generate_device_info_file()

def read_device_info_file():
    """
    read_device_info_file
    Reads device info from disk. Returns a DeviceInfo object.
    """
    device_info = None
    try:
        with uio.open(DEVICE_INFO_PATH, mode='r') as infile:
            device_data = ujson.loads(infile.read())
            device_info = DeviceInfo(device_data)
        infile.close()
    except ValueError as err:
        print("Could not parse device info file JSON", err)
    except OSError as err:
        print("Could not open device info file.", err)

    return device_info

def does_device_info_file_exist():
    """
    does_device_info_file_exist
    returns true if device info file exists, false otherwise.
    """
    return does_file_exist(DEVICE_INFO_PATH)

def does_file_exist(filename):
    """
    does_file_exist
    Returns true if the given filename exists, false otherwise.
    """
    exists = False
    try:
        with uio.open(filename, mode='r') as infofile:
            exists = True
        infofile.close()
    except OSError:
        pass
    return exists
