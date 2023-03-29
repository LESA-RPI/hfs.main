from machine import Pin, ADCBlock
import time

block = ADCBlock(2, bits=12)

PHOTODIODE_RESULT = block.connect(6, Pin(14, Pin.IN))

RESET = Pin(16, Pin.IN)

LED_POW_SUPPLY_PIN = Pin(13, Pin.IN)

LED1 = Pin(26, Pin.OUT)
LED2 = Pin(27, Pin.OUT)
LED3 = Pin(32, Pin.OUT)
LED4 = Pin(25, Pin.OUT)

SCL = Pin(22, Pin.IN)
SDA = Pin(21, Pin.OUT)
XSHUT_PIN = Pin(19, Pin.IN)
GPIO1 = Pin(18, Pin.IN)
AVDD_PIN = Pin(17, Pin.IN)
IOVDD_PIN = Pin(12,Pin.IN)