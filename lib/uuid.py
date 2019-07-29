"""
UUID
A class for generating UUIDs
"""
import os
import ubinascii # pylint: disable=E0401

 # pylint: disable=C0103
class UUID: # pylint: disable=C1001
    """
    UUID

    A class for generating UUIDs
    """
    def __init__(self, bytes): # pylint: disable=W0622
        if len(bytes) != 16:
            raise ValueError('bytes arg must be 16 bytes long')
        self._bytes = bytes

    @property
    def hex(self):
        """
        hex
        returns hex representation of the UUID bytes
        """
        return ubinascii.hexlify(self._bytes).decode()

    def __str__(self):
        h = self.hex
        return '-'.join((h[0:8], h[8:12], h[12:16], h[16:20], h[20:32]))

    def __repr__(self):
        return "<UUID: %s>" % str(self)


def uuid4():
    """Generates a random UUID compliant to RFC 4122 pg.14"""
    random = bytearray(os.urandom(16))
    random[6] = (random[6] & 0x0F) | 0x40
    random[8] = (random[8] & 0x3F) | 0x80
    return UUID(bytes=random)

def uuid4_str():
    """
    Generates a string UUID
    """
    return str(uuid4())

def uuid2bytes(uuid):
    """
    uuid2bytes
    Converts uuid string to a little-endian bytes object
    """
    uuid = uuid.encode().replace(b'-', b'')
    tmp = ubinascii.unhexlify(uuid)
    return bytes(reversed(tmp))

def generate_device_id():
    """
    generate_device_id
    Generates a random 8 byte id string
    """
    return ubinascii.hexlify(os.urandom(8)).decode()
