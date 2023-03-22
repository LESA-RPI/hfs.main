import struct
import time
from machine import unique_id

import device_pins as pins

ID = abs(hash(unique_id())) % 65534

def pack(distance, chlf):
    return struct.pack("<HIHH", ID, time.time(), distance, chlf)

def readPhotodiode():
    return pins.PHOTODIODE_RESULT.read_u16()

def readSonar():
    return 0

def readAndSend(server, pipe):
    distance, chlf = readSonar(), readPhotodiode()
    print(f"Writing '{distance}', {chlf} to peripheral...")
    try:
        pipe.write(pack(distance, chlf))
        pipe.notify(server)
    except Exception as error:
        print(f"[ERROR] Write to pipe failed because of {error}") 