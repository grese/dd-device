"""
helpers.py

Helper functions
"""

import utime, machine # pylint: disable=E0401,W0611,C0410

def current_timestamp():
    """
    current_timestamp
    Returns current timestamp in ISO8601 format
    """
    return "%d-%02d-%02dT%02d:%02d:%02dZ" % utime.localtime()[:6]

def set_current_time(time_tuple):
    """
    set_current_time
    Sets system time
    """
    rtc = machine.RTC()
    rtc.init(time_tuple)

def is_time_set():
    """
    is_time_set
    returns true if the RTC has alread already been set. false otherwise.
    """
    rtc = machine.RTC()
    now = rtc.now()
    if now[0] == 1970:
        return False
    return True
