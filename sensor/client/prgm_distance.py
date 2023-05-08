#taken from https://github.com/uceeatz/VL53L0X/blob/master/main.py
import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins
import time
from machine import Pin
from machine import I2C
import VL53L0X

delt_t = 0
count = 0
sumCount = 0;  # used to control display output rate
deltat = 0.0
sum = 0.0         # integration interval for both filter schemes
lastUpdate = 0
firstUpdate = 0 # used to calculate integration interval
Now = 0                         # used to calculate integration interval

i2c = I2C.init(pins.SCL, pins.SDA, freq=400000)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, frequency, sampleSize):    
    print("[prgm_distance] start")
    # pipe.write("data")
    # Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()
    pipe.notify(server)
    print("[prgm_distance] stop")