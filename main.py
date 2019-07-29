"""
main.py

This code runs immediately after board boots up.
"""
# Add ./src to the path
import sys
sys.path.append('/flash/src')

# pylint: disable=C0413
import time
import pycom # pylint: disable=F0401
from src.device import Device

# Turn off blinking LED.
pycom.heartbeat(False) # pylint: disable=E1101

DATA_CACHE_DURATION = 7 # days
DATA_INTERVAL = 10 # seconds

# Initialize Device object
DD_DEVICE = Device(DATA_CACHE_DURATION, DATA_INTERVAL)

for r in range(20):
    DD_DEVICE.read_sensor_data() # create humidity_temp reading.
    DD_DEVICE.check_for_event() # check sensor data for event
    time.sleep(DATA_INTERVAL) # sleep until time to create new reading
