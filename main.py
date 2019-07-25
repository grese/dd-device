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

EVENT_CACHE_DURATION = 7 # days
EVENT_INTERVAL = 15 # seconds

# Initialize Device object
DD_DEVICE = Device(EVENT_CACHE_DURATION, EVENT_INTERVAL)

for r in range(10):
    DD_DEVICE.create_event() # create humidity_temp event.
    time.sleep(EVENT_INTERVAL) # sleep until time to create new event
