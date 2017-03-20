import logging
import os
import struct

kLog = logging.getLogger(__name__)


class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Not enough bytes in fp to satisfy read request'


class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        'int8': '!b',
        'uint8': '!B',
        'int16': '!h',
        'uint16': '!H',
        'int32': '!i',
        'uint32': '!I',
        'int64': '!q',
        'uint64': '!Q',
        'float': '!f',
        'double': '!d',
        'char': '!s'}

    def __init__(self, fpName):
        self.fp = open(fpName, 'rb')

    def read(self, typeName):
        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.fp.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)[0]

    def seek(self, skip):
        self.fp.seek(skip)

    def __del__(self):
        self.fp.close()


def parser(filename):
    if os.stat(filename).st_size < 500:
        return

    values = {}

    binaryReader = BinaryReader(filename)
    try:
        binaryReader.seek(220 + 19)
        # Seconds since epoch.
        values['ts'] = binaryReader.read('uint32')
        binaryReader.seek(220 + 44)
        # Current in mA.
        values['current'] = binaryReader.read('uint16')
        binaryReader.seek(220 + 54)
        # Voltage in tenth of V.
        values['voltage'] = binaryReader.read('uint16')
        binaryReader.seek(220 + 68)
        # Power in W.
        values['power'] = binaryReader.read('uint16')
    except BinaryReaderEOFException:
        # One of our attempts to read a field went beyond the end of the file.
        kLog.error("Error: File seems to be corrupted.")

    return values
