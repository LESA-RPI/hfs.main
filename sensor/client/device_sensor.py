import struct
import time
from machine import unique_id

import device_pins as pins
import pycom
from machine import Pin
from machine import I2C
import VL53L0X

i2c = I2C(0)
i2c = I2C(0, I2C.MASTER)
i2c = I2C(0, pins=('P10','P9'))
i2c.init(I2C.MASTER, baudrate=9600)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)

CURRENT_VERSION = 0
ID = abs(hash(unique_id())) % 65534

def pack(distance, chlf):
    return struct.pack("<HIHHH0s", ID, time.time(), distance, chlf, 0, "")

def readPhotodiode():
    return pins.PHOTODIODE_RESULT.read_u16()

def readSonar():
    try:
        tof.start()
        distValue = tof.read()
        print(distValue)
        tof.stop()
        return distValue
    except Exception as error:
        pass
    return 0

def readAndSend(server, pipe):
    distance, chlf = readSonar(), readPhotodiode()
    log(server, pipe, f"Writing '{distance}', {chlf} to peripheral...")
    try:
        pipe.write(pack(distance, chlf))
        pipe.notify(server)
    except Exception as error:
        log(server, pipe, f"[ERROR] Write to pipe failed because of {error}") 

def log(server, pipe, msg):
    print(msg)
    try:
        packed_msg = struct.pack(f"<HIHHH{len(msg)}s", ID, 0, 0, 0, len(msg), msg.encode())
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
    
