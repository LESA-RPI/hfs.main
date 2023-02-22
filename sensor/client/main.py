# Bluetooth peripheral code for fluorescence sensor 
print("INFO: Starting device...")


#import asyncio
#import ble_service
from .noise import start
#from .frequency import startFrequencyTest

print(2)
print(3)

#tests.startDistanceTest()
#tests.startFarfieldTest()
#tests.startFrequencyTest()
#tests.startNoiseTest()
if __name__ == '__main__':
    start()

#asyncio.run(ble_service.main())