import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins
from machine import Timer
import uasyncio
import math

frequency = 15
counter = 0
LEDON = True
led_on_time = 1.5
samples = 5
led_wait_measure_time = 0.6
led_measurement_time = led_on_time-led_wait_measure_time
led_between_measure_time = round((led_measurement_time*1000)/samples)


def timerCallback(server, pipe):
    global counter, LEDON
    LEDON = not LEDON
    counter = counter + 1 #increments counter used for determining when to stop measurements

async def measurements1(tim, server, pipe):
    while (counter-1) < round(frequency*led_wait_measure_time):
        pass
    print("starting measurements")
    for i in range(0, samples):
        sensor.readAndSend(server, pipe)
        await sleep_between_measurements(led_between_measure_time)
    tim.deinit() 

async def sleep_between_measurements(led_time):
    await uasyncio.sleep_ms(led_time)

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, data: int):    
    sensor.log(server, pipe, "[INFO] starting prgm_photodiode")
    tim = Timer(1) #timer used to count when LED sleeps and takes measurements
    tim.init(freq = frequency, mode = Timer.PERIODIC, callback = lambda t: timerCallback(server, pipe))
    sensor.readSonar()
    await measurements1(tim, server, pipe)
    # pipe.write("data")
    #pipe.notify(server)
    sensor.log(server, pipe, "[INFO] ending prgm_photodiode")