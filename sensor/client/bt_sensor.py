import pins
import struct
import time
from machine import unique_id

ID = abs(hash(unique_id())) % 65534

def pack(distance, chlf):
    return struct.pack("<HIHH", ID, time.time(), distance, chlf)

def readPhotodiode():
    return pins.RESULT.read_u16()

def readSonar():
    return 100

def sendValues(connection, characteristic):
    distance, chlf = readSonar(), readPhotodiode()
    print(f"Writing '{distance}', {chlf} to peripheral...")
    characteristic.write(pack(distance, chlf))
    characteristic.notify(connection)
