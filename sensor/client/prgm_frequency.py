import uasyncio
import math
import machine
from machine import Timer

import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins

frequency_list = [15, 50, 100, 200, 400, 800, 1000, 1200, 1400, 600, 700, 650]
led_on_time = 10 #10 sec
led_off_start_time = 10*60*1000 #10 min
led_off_time = 10 #10 sec
#led_off_time = 5*60*1000 #5 min
led_between_measure_time = 800 #TT
led_wait_measure_time = 200
samples = 5
counter = 0
results = []
average_result = 0
LEDON = True

def led_blinking():
    if LEDON == True:
        pins.LED1.on()
        pins.LED2.on()
        pins.LED3.on()
        pins.LED4.on()
        print("on")
    else:
        pins.LED1.off()
        pins.LED2.off()
        pins.LED3.off()
        pins.LED4.off()
        print("off")

async def measurements():
    await sleep_between_measurements(led_wait_measure_time)
    for i in range(0, samples):
        results.append(sensor.readPhotodiode())
        print("Results ", results[i])
        #total_result = total_result + results[i]
        #machine.lightsleep(led_between_measure_time)
        await sleep_between_measurements(led_between_measure_time)

async def sleep(curFreq):
    global counter, led_off_time, led_wait_measure_time, results, led_between_measure_time
    while(counter >= led_off_time*curFreq):
        pins.LED1.off()
        pins.LED2.off()
        pins.LED3.off()
        pins.LED4.off()
        print("OFF")
        counter = 0
    #machine.lightsleep(led_wait_measure_time)
    #average_result = total_result/samples
    #print("Average result: ",average_result)
    #total_result = 0
    #machine.deepsleep(led_off_time)
    await sleep_between_measurements(led_off_time)
    counter = 0 #maybe before deep sleep?

def timerCallback(curFreq):
    global counter, LEDON
    led_blinking()
    LEDON = not LEDON
    if counter == curFreq*0.6:
        measurements()
    counter = counter + 1 #increments counter used for determining when to stop measurements
    print(counter)

async def sleep_between_measurements(led_time):
    await uasyncio.sleep_ms(led_time)

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, data: int):    
    print("[prgm_frequency] start")
    await sleep_between_measurements(led_off_time) #sleeps for 5 minutes
    for curFreq in frequency_list: #all the frequencies in test
        tim = Timer(1) #timer used to count when LED sleeps and takes measurements
        tim.init(freq = curFreq, mode = Timer.PERIODIC, callback = lambda t:timerCallback(curFreq))
        await uasyncio.sleep(led_on_time)
        tim.deinit()
        print(counter)
        await sleep(curFreq) #sleeps for 10 minutes
    #pipe.notify(server)
    print("[prgm_frequency] stop")
    
