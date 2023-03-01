import uasyncio
import math
import machine
from machine import Timer

import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins

frequency_list = [15, 50, 100, 200, 400, 800, 1000, 1200, 1400, 600, 700, 650]
led_on_time = 1000 #1 sec
led_off_start_time = 10*60*1000 #10 min
led_off_time = 10000 #5 min
#led_off_time = 5*60*1000 #5 min
led_between_measure_time = 800/5 #TT
led_wait_measure_time = 200
samples = 5
counter = 0
results = []
average_result = 0

async def led_blinking(led, freq):
    while counter < led_off_time:
        led.on()
        await uasyncio.sleep_ms(round((1/freq)*10**3))
        print("LED ", led, " on")
        led.off()
        await uasyncio.sleep_ms(round((1/freq)*10**3))
        print("LED", led, " off")

async def cycle(led1, led2, led3, led4, freq):
    uasyncio.create_task(led_blinking(led1, freq))
    uasyncio.create_task(led_blinking(led2, freq))
    uasyncio.create_task(led_blinking(led3, freq))
    uasyncio.create_task(led_blinking(led4, freq))


def sleep():
    while(counter >= led_off_time):
        pins.LED1.off()
        pins.LED2.off()
        pins.LED3.off()
        pins.LED4.off()
        counter = 0
    machine.lightsleep(led_wait_measure_time)
    for i in range(samples):
        results[i] =  sensor.readPhotodiode()
        print("Results ", results[i])
        #total_result = total_result + results[i]
        machine.lightsleep(led_between_measure_time)
    #average_result = total_result/samples
    #print("Average result: ",average_result)
    #total_result = 0
    machine.deepsleep(led_off_time)
    counter = 0 #maybe before deep sleep?

def timerCallback():
    counter = counter + 1 #increments counter used for determining when to stop measurements

# entry point for the program
# run this program once and only once, server will decide how to loop
def run(server, pipe, data: int):    
    print("[prgm_frequency] start")
    machine.lightsleep(led_off_time) #sleeps for 5 minutes
    for curFreq in frequency_list: #all the frequencies in test
        tim = Timer(1) #timer used to count when LED sleeps and takes measurements
        timer = tim.channel(channel = machine.TIMER.A, freq = curFreq, mode = Timer.PWM, pulse_width_percent=50)
        tim.callback(timerCallback)
        print(counter)
        cycle(pins.LED1, pins.LED2, pins.LED3, pins.LED4) #threads LEDs blinking
        sleep() #sleeps for 10 minutes
    pipe.notify(server)
    print("[prgm_frequency] stop")
    