"""
DHT
Class for reading DHT humidity/temperature sensor data
"""
import pycom
import utime # pylint: disable=E0401
from machine import Pin # pylint: disable=E0401

def bits_to_bytes(bits):
    """
    bits_to_bytes
    Turns a stream of bits into a byte array
    """
    the_bytes = []
    byte = 0

    for i in range(0, len(bits)): # pylint: disable=C0200
        byte <<= 1
        if bits[i]:
            byte |= 1
        if (i % 8) == 7:
            the_bytes.append(byte)
            byte = 0
    return the_bytes

def calculate_checksum(the_bytes):
    """
    calculate_checksum
    Calculates the checksum for the given byte array
    """
    return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255

class DHTResult: # pylint: disable=C1001, R0903
    'DHT sensor result returned by DHT.read() method'

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        """
        is_valid
        Returns true if the DHT result is valid.  False otherwise.
        """
        return self.error_code == DHTResult.ERR_NO_ERROR

 # pylint: disable=C0103
class DHT: # pylint: disable=C1001,R0903
    """
    DHT
    DHT sensor (dht11, dht21,dht22) reader class for Pycom
    """

    __dhttype = 0

    def __init__(self, pin, sensor=0):
        self.__pin = Pin(pin, mode=Pin.OPEN_DRAIN)
        self.__dhttype = sensor
        self.__pin(1)
        utime.sleep(1.0)

    def read(self):
        """
        read
        Reads data from DHT sensor
        """
        # pull down to low
        self.__send_and_sleep(0, 0.019)
        data = pycom.pulses_get(self.__pin, 100) # pylint: disable=E1101
        self.__pin.init(Pin.OPEN_DRAIN)
        self.__pin(1)
        bits = []
        for a, b in data:
            if a == 1 and 18 <= b <= 28:
                bits.append(0)
            if a == 1 and 65 <= b <= 75:
                bits.append(1)
        if len(bits) != 40:
            return DHTResult(DHTResult.ERR_MISSING_DATA, 0, 0)
        # we have the bits, calculate bytes
        the_bytes = bits_to_bytes(bits)
        # calculate checksum and check
        checksum = calculate_checksum(the_bytes)
        if the_bytes[4] != checksum:
            return DHTResult(DHTResult.ERR_CRC, 0, 0)
        # ok, we have valid data, return it
        [int_rh, dec_rh, int_t, dec_t, csum] = the_bytes # pylint: disable=E0632,W0612
        if self.__dhttype == 0:
            #dht11
            rh = int_rh                 #dht11 20% ~ 90%
            t = int_t                   #dht11 0..50 deg C
        else:
            #dht21,dht22
            rh = ((int_rh * 256) + dec_rh)/10
            t = (((int_t & 0x7F) * 256) + dec_t)/10
            if (int_t & 0x80) != 0:
                t = -t
        return DHTResult(DHTResult.ERR_NO_ERROR, t, rh)


    def __send_and_sleep(self, output, mysleep):
        self.__pin(output)
        utime.sleep(mysleep)
