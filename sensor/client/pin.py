# Pin

from machine import Pin, ADCBlock
import time
block = ADCBlock(2, bits=12)
RESULT = block.connect(6, Pin(14, Pin.IN))
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

""" def main():
    result_pin = Pin(14, Pin.IN)
    measured_result = ADC2(result_pin)
    result = measured_result.read_u16()

    reset_pin = Pin(16, Pin.IN)
    reset = reset_pin.read_u16()

    led_pow_supply_pin = Pin(13, Pin.IN)
    led_pow_supply = led_pow_supply_pin.read_u16()

    led1_pin = Pin(26, Pin.OUT_PP)
    #led1_pin.LED(1)
    #led1 = led1_pin.read_u16()

    led2_pin = Pin(27, Pin.OUT_PP)
    #led2_pin.LED(2)
    #led2 = led2_pin.read_u16()

    led3_pin = Pin(32, Pin.OUT_PP)
    #led3_pin.LED(3)
    #led3 = led3_pin.read_u16()

    led4_pin = Pin(25, Pin.OUT_PP)
    #led4_pin.LED(4)
    #led4 = led4_pin.read_u16()

    gpio1_pin = Pin(18, Pin.IN)
    gpio = gpio1_pin.read_u16()

    for x in range(5):
        print(result)
        print(reset)
        print(led_pow_supply)
        print(led1_pin)
        print(led2_pin)
        print(led3_pin)
        print(led4_pin)
        print(gpio)


    #f = open('data.txt', 'w')
    #f.write(str(result))
    #f.close()
 """