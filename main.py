"""
main.py

This code runs immediately after board boots up.
"""

import sys

sys.path.append('/flash/src')

from src.device import Device
import time
import pycom

# Turn off blinking LED.
pycom.heartbeat(False)

# Initialize Device object
dd_device = Device()

for r in range(10):
    dd_device.create_event() # create humidity_temp event.
    time.sleep(15) # sleep for 15 seconds
