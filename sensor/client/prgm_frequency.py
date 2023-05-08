import uasyncio
import math
import machine
from machine import Timer

import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins

frequency_list = [15, 50, 100, 200, 400, 800, 1000, 1200, 1400, 600, 700, 650]
led_on_time = 1.5 #10 sec
led_off_start_time = 10*60*1000 #10 min
#led_off_start_time = 60*1000 #1 min for testing purposes
led_wait_measure_time = 0.6
led_measurement_time = led_on_time-led_wait_measure_time
led_between_measure_time = round((led_measurement_time*1000)/samples) #TT
counter = 0
average_result = 0
samples = []
sampleSize = round(pow(2, 13) / 16) # max length of a u16 list (this isn't actually the max, but anything higher risks memory allocation errors)
LEDON = True

def led_blinking():
    if LEDON == True:
        pins.LED1.on()
        pins.LED2.on()
        pins.LED3.on()
        pins.LED4.on()
    else:
        pins.LED1.off()
        pins.LED2.off()
        pins.LED3.off()
        pins.LED4.off()

   
async def measurements(curFreq, server, pipe):
    while (counter-1) < round(curFreq*led_wait_measure_time):
        pass
    sensor.log(server, pipe, "[INFO] starting measurements")
    for i in range(0, sampleSize):
        while(LEDON == False):
            await uasyncio.sleep_ms(0)
        value = sensor.readPhotodiode()
        samples.append(value)
        await sleep_between_measurements(led_between_measure_time)  


async def sleep(curFreq, tim, server, pipe):
    global counter, led_on_time, led_off_start_time
    while(counter < led_on_time*curFreq):
        await uasyncio.sleep(0)
    pins.LED1.off()
    pins.LED2.off()
    pins.LED3.off()
    pins.LED4.off()
    tim.deinit()
    pins.LED_POWER_SWITCH.off()
    sensor.log(server, pipe, "[INFO] LEDs off")
    counter = 0
    await sleep_between_measurements(led_off_start_time)
    counter = 0 #maybe before deep sleep?

def timerCallback(curFreq, server, pipe):
    global counter
    counter = counter + 1 #increments counter used for determining when to stop measurements
    if counter % 2:
        led_blinking()
        global LEDON
        LEDON = not LEDON
    elif counter > led_wait_measure_time * curFreq * 2:
        measurements(curFreq)
    

async def sleep_between_measurements(led_time):
    await uasyncio.sleep_ms(led_time)
    print("why hello there")

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, frequency):   
    global samples 
    sensor.log(server, pipe, "[INFO] starting prgm_frequency")
    await sleep_between_measurements(led_off_start_time) #sleeps for 10 minutes
    for curFreq in frequency_list: #all the frequencies in test
        sensor.log(server, pipe, f"[INFO] Actual frequency: {curFreq}")
        tim = Timer(1) #timer used to count when LED sleeps and takes measurements
        tim.init(freq = curFreq, mode = Timer.PERIODIC, callback = lambda t: timerCallback(curFreq, server, pipe))
        sensor.readSonar()
        pins.LED_POWER_SWITCH.on()
        await measurements(curFreq, server, pipe)
        await sleep(curFreq, tim, server, pipe) #sleeps for 10 minutes
    pipe.notify(server)
    sensor.log(server, pipe, "[INFO] ending prgm_frequency")
    
