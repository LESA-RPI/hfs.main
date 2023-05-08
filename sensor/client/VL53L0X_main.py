#taken from https://github.com/uceeatz/VL53L0X/blob/master/main.py
import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins
import time
from machine import Pin
from machine import I2C
import VL53L0X


i2c = I2C.init(pins.SCL, pins.SDA, baudrate=9600)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)


while True:
# Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()






    #q = tof.set_signal_rate_limit(0.1)
    #
    # time.sleep(0.1)