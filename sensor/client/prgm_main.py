import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins
from machine import Timer, PWM, Pin
import uasyncio
import math

frequency = 400
counter = 0
LEDON = True
led_on_time = 3
samples = 5
led_wait_measure_time = 0.6
led_measurement_time = led_on_time-led_wait_measure_time
led_between_measure_time = round((led_measurement_time*1000)/samples)

def led_blinking():
    if LEDON == True:
        pins.LED_REF.on()

    else:
        pins.LED_REF.off()

def timerCallback(server, pipe):
    global counter, LEDON
    LEDON = not LEDON
    led_blinking()
    counter = counter + 1 #increments counter used for determining when to stop measurements

async def measurements1(tim, server, pipe):
    PWM(Pin(7), freq=10000, duty=1023) #duty between 0 and 1023
    while (counter-1) < round(frequency*led_wait_measure_time):
        pass
    print("starting measurements")
    for i in range(0, samples):
        while(LEDON == False):
            await uasyncio.sleep_ms(0)
        sensor.readAndSend(server, pipe)
        await sleep_between_measurements(led_between_measure_time)
    PWM(Pin(7), freq=10000, duty=0)


async def sleep_between_measurements(led_time):
    await uasyncio.sleep_ms(led_time)
    print("why hello there")

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, data: int):    
    print("[prgm_main] start")
    tim = Timer(0) #timer used to count when LED sleeps and takes measurements
    tim.init(freq = frequency*2, mode = Timer.PERIODIC, callback = lambda t: timerCallback(server, pipe))#Produce a 400Hz pulse, interesting implementation
    sensor.readSonar()
    await measurements1(tim, server, pipe)
    print("hello world")
    #pipe.notify(server)
    tim.deinit() 
    print("[prgm_main] stop")