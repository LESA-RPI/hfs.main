from machine import Pin, ADC2
RESULT = ADC2(Pin(14, Pin.IN))
def start():
    print("Hello World!")
    