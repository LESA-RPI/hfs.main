from machine import Pin, ADC, PWM

import time

# frequency testing
fs = [15, 50, 100, 200, 400, 800, 1000, 1200, 1400, 1600, 1800, 2000]

# set up pins
#measured_result = ADC(Pin(14, Pin.IN))
led_flash = PWM(Pin(33, Pin.OUT))

for f in fs:
    print(f"Flashing with freq={f}...")
    led_flash.init(freq=f)
    asyncio.sleep(2)
    led_flash.deinit()
