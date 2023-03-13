#manually run import main or import boot in terminal in order to update cache
# Bluetooth peripheral code for fluorescence sensor 
print("[INFO] Starting device...")


#import asyncio
#import ble_service
import prgm_frequency
import bt_service as ble
import uasyncio as asyncio


print(2)
print(3)

#tests.startDistanceTest()
#tests.startFarfieldTest()
#tests.startFrequencyTest()
#tests.startNoiseTest()
if __name__ == '__main__':
    print("[INFO] running!")
    
    asyncio.run(ble._start())
    print("fin")
    prgm_frequency.run()

#asyncio.run(ble_service.main())