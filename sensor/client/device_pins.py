from machine import Pin, ADCBlock, PWM
import time

#ESP32C3
#ESP32's onboard ADC block
block = ADCBlock(0, bits=12)
PHOTODIODE_RESULT = block.connect(0, Pin(0, Pin.IN))
#LED_REF
LED_REF = Pin(6, Pin.OUT)
ESP_PWM_DIM = PWM(Pin(7), freq=1000, duty=0)
NeopixelLED = Pin(8, Pin.OUT)
#I2C
SCL = Pin(4, Pin.IN)
SDA = Pin(5, Pin.OUT)
#main interrupt pin
INT = Pin(10, Pin.IN)

#XSHUT_PIN = Pin(7, Pin.IN)
#GPIO1 = Pin(18, Pin.IN)
#POWER_GPIO1 = Pin(18, Pin.OUT)
#AVDD_PIN = Pin(9, Pin.IN)
#IOVDD_PIN = Pin(10,Pin.IN)

#'''

''' ToF sensor test code
from machine import Pin, ADCBlock
from machine import I2C
import VL53L0X
block = ADCBlock(1, bits=12)
PHOTODIODE_RESULT = block.connect(0, Pin(0, Pin.IN))
i2c = I2C(0, sda=Pin(5), scl=Pin(4))
tof = VL53L0X.VL53L0X(i2c)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)

while(1):
    print("ADC:\t\t"+str(PHOTODIODE_RESULT.read()),end='\t')
    #tof.start()
    print("distance\t"+str(tof.read()))
    #tof.stop()
    for i in range(1, 10000):
        pass
'''
'''
LED test code

from machine import PWM
pwm = PWM(Pin(7), freq=1000, duty=512)
pwm.init(freq=500, duty=256)
pwm = PWM(Pin(6), freq=1000, duty=512)
pwm.init(freq=500, duty=256)

or 

io6 = Pin(6, Pin.OUT)
io7 = Pin(7, Pin.OUT)
io6.value(1)
io7.value(1)
'''
#RESET = Pin(3, Pin.IN)

print("[INFO] Device_pins.py imported")