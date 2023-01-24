# Bluetooth peripheral code for fluorescence sensor 

import asyncio
import ble_service
import tests

#tests.startDistanceTest()
#tests.startFarfieldTest()
#tests.startFrequencyTest()
#tests.startNoiseTest()

asyncio.run(ble_service.main())