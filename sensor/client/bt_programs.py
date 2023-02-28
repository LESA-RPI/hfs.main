import prgm_distance
import prgm_farfield
import prgm_flashtest
import prgm_frequency
import prgm_noise
import prgm_utils
import prgm_main


PROGRAMS = {
    0: prgm_utils.setLedFreqency,
    10: prgm_main.run,
    11: prgm_distance.run,
    12: prgm_farfield.run,
    13: prgm_flashtest.run,
    14: prgm_frequency.run,
    15: prgm_noise.run
}

DEFAULT = PROGRAMS[10]

def get():
    pass

def setDefault(data):
    DEFAULT = PROGRAMS[int(data)]
    