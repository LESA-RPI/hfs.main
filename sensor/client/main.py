#manually run import main or import boot in terminal in order to update cache
# Bluetooth peripheral code for fluorescence sensor 
print("INFO: Starting device...")

import uasyncio as asyncio

#import asyncio
#import ble_service
import prgm_frequency
import bt_service as ble


print(2)
print(3)

#tests.startDistanceTest()
#tests.startFarfieldTest()
#tests.startFrequencyTest()
#tests.startNoiseTest()
if __name__ == '__main__':
    prgm_frequency.start()
    asyncio.run(ble.start())

#asyncio.run(ble_service.main())