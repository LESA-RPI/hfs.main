# Pin

from machine import Pin, ADC 
import time

def main():
    result_pin = Pin(14, Pin.IN)
    measured_result = ADC(result_pin)
    result = measured_result.read_u16()

    for _ in range(5):
        print(result)

    #f = open('data.txt', 'w')
    #f.write(str(result))
    #f.close()
