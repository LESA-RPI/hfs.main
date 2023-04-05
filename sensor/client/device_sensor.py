import struct
import time
from machine import unique_id

import device_pins as pins

CURRENT_VERSION = 0
ID = abs(hash(unique_id())) % 65534

def pack(distance, chlf):
    return struct.pack("<HIHHp", ID, time.time(), distance, chlf, "")

def readPhotodiode():
    return pins.PHOTODIODE_RESULT.read_u16()

def readSonar():
    return 0

def readAndSend(server, pipe):
    distance, chlf = readSonar(), readPhotodiode()
    log(f"Writing '{distance}', {chlf} to peripheral...")
    try:
        pipe.write(pack(distance, chlf))
        pipe.notify(server)
    except Exception as error:
        log(f"[ERROR] Write to pipe failed because of {error}") 

def log(server, pipe, msg):
    print(msg)
    try:
        packed_msg = struct.pack("<HIHHp", ID, 0, 0, 0, msg)
        try:
            pipe.write(packed_msg)
            try: 
                pipe.notify(server)
            except Exception as error:
                print(f"[ERROR] Notifying server failed because of {error}") 
        except Exception as error:
            print(f"[ERROR] Write to pipe failed because of {error}") 
    except Exception as error:
        print(f"[ERROR] Packing message to pipe failed because of {error}") 
    
