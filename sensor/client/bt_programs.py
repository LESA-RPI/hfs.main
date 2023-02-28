import struct

import prgm_distance
import prgm_farfield
import prgm_flashtest
import prgm_frequency
import prgm_noise
import prgm_main

PROGRAMS = {
    10: (prgm_main.run, 'Main'),
    11: (prgm_distance.run, 'Distance Test'),
    12: (prgm_farfield.run, 'Farfield Test'),
    13: (prgm_flashtest.run, 'Flash Test'),
    14: (prgm_frequency.run, 'Frequency Test'),
    15: (prgm_noise.run, 'Noise Test')
}

DEFAULT = PROGRAMS[10][0]

def get(server, pipe):
    print("[bt_get] start")
    global PROGRAM
    values = list(PROGRAM.values())
    pipe.write(struct.pack("<" + ("p"*len(values))), *values)
    pipe.notify(server)
    print("[bt_get] stop")
    

def setDefault(server, pipe, data):
    print("[bt_setdefault] start")
    DEFAULT = PROGRAMS[int(data)][0]
    pipe.notify(server)
    print("[bt_setdefault] stop")
    