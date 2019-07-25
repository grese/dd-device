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

# Initialize Device object
DD_DEVICE = Device()

for r in range(10):
    DD_DEVICE.create_event() # create humidity_temp event.
    time.sleep(15) # sleep for 15 seconds
