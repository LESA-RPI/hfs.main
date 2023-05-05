import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins
from machine import Timer
import uasyncio
import math

lock = uasyncio.Lock()
counter = 0
LEDON = True
led_on_time = 1.5
sampleCount = 5
led_wait_measure_time = 0.6
led_measurement_time = led_on_time-led_wait_measure_time
led_between_measure_time = round((led_measurement_time*1000)/sampleCount)
measurement_collection = []

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

def timerCallback(server, pipe):
    global counter
    counter = counter + 1 #increments counter used for determining when to stop measurements
    if counter % 2:
        led_blinking()
    else:
        measurements()


def measurements():
    global samples
    # APPEND IS ATOMIC IN PYTHON!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    value = sensor.readPhotodiode()
    samples.append(value)
    # todo: uncomment this line to enable 'study' mode, not reccomended!
    # sensor.send(server, pipe, sensor.CURRENT_DISTANCE, avg)
    print(value)

async def measurements1(frequency, tim, server, pipe):
    while (counter-1) < round(frequency * led_wait_measure_time):
        pass
    print("starting measurements")
    for i in range(0, sampleCount):
        while(LEDON == False):
            await uasyncio.sleep_ms(0)
        sensor.readAndSend(server, pipe)
        await sleep_between_measurements(led_between_measure_time)
    tim.deinit() 
    pins.LED_POWER_SWITCH.off()
    

async def sleep_between_measurements(led_time):
    await uasyncio.sleep_ms(led_time)
    print("why hello there")

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, frequency, sampleSize):
    global samples
    samples = []
    global sampleCount
    print("[prgm_main] start")
    if sampleSize != 0:
        sampleCount = sampleSize
    if frequency == 0:
        frequency = 1000
    tim = Timer(1) #timer used to count when LED sleeps and takes measurements
    tim.init(freq = frequency * 2, mode = Timer.PERIODIC, callback = lambda t: timerCallback(server, pipe))
    sensor.readSonar()
    pins.LED_POWER_SWITCH.on()

    while (counter-1) < round(frequency * led_wait_measure_time):
        pass
    num_samples = len(samples)
    tim.deinit()
    pins.LED_POWER_SWITCH.off()
    sensor.log(server, pipe, f"Read {num_samples}/{round(frequency * led_wait_measure_time)} samples")

    # get the average
    # todo: get std.dev, median, all that other jazz!
    avg = 0
    null_samples = 0
    for i in range(num_samples):
        if samples[i] == 0:
            null_samples += 1
        else:
            avg += samples[i]
    
    # div by 0 is bad!
    try: 
        avg /= num_samples - null_samples
    except ZeroDivisionError:
        sensor.log(server, pipe, "Wow this is really bad, good luck mate!")
    
    # send it off!!
    sensor.send(server, pipe, sensor.CURRENT_DISTANCE, round(avg))

    # pipe.write("data")
    print("hello world")
    #pipe.notify(server)
    print("[prgm_main] stop")