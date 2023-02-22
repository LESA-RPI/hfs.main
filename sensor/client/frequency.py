import pin
import pyb
import uasyncio
import math
import machine
from machine import Timer
frequency_list = [15, 50, 100, 200, 400, 800, 1000, 1200, 1400, 600, 700, 650]
led_on = 1000 #1 sec
led_off_start = 10*60*1000 #10 min
led_off = 5*60*1000 #5 min
led_between_measure = 800/5 #TT
led_wait_measure = 200
samples = 5
counter = 0
results = []
average_result = 0

async def led_blinking(led, freq):
    while counter < led_off:
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
    counter = 0
    while(counter >= led_off):
        pin.LED1.off()
        pin.LED2.off()
        pin.LED3.off()
        pin.LED4.off()
        counter = 0
    machine.lightsleep(led_wait_measure)
    for i in range(samples):
        results[i] =  pin.RESULT
        print(results[i])
        #total_result = total_result + results[i]
        machine.lightsleep(led_between_measure)
    #average_result = total_result/samples
    #print("Average result: ",average_result)
    #total_result = 0
    machine.deepsleep(led_off)

def start():
    #machine.deepsleep(led_off)
    for curFreq in frequency_list:
        tim = Timer(1)
        timer = tim.channel(channel = machine.TIMER.A, freq = curFreq, mode = Timer.PWM, pulse_width_percent=50)
        tim.callback(timerCallback)
        cycle(pin.LED1, pin.LED2, pin.LED3, pin.LED4)
        sleep()

def timerCallback():
    counter = counter + 1
    
