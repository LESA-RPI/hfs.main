# Bluetooth peripheral code for fluorescence sensor 

import aioble
import uasyncio as asyncio
import bluetooth as bt

from machine import Pin, ADC

import random
import struct

# UUID constants
_COMM_UUID = bt.UUID("26c00001-ece0-4f7a-b663-223de05387cc")
_COMM_RW_UUID = bt.UUID("26c00002-ece0-4f7a-b663-223de05387cc")

# register GATT service
comm_service = aioble.Service(_COMM_UUID)
comm_characteristic = aioble.Characteristic(
        comm_service,
        _COMM_RW_UUID,
        read=True,
        write=True,
        notify=True
)
aioble.register_services(comm_service)

# set up pins
measured_result = ADC( Pin(14, Pin.IN) )

# TODO
# tof_scl = Pin(22
# tof_sda = Pin(21
# tof_shutdown = Pin(19
# 

def encode(data):
    return struct.pack("<h", int(data * 100))

async def write(conn):
    while True:
        result = encode( measured_result.read_u16() )
        print(f"Writing '{result}' to peripheral...")
        comm_characteristic.write(result)
        comm_characteristic.notify(conn)
        await asyncio.sleep_ms(500) # change time accordingly

async def advertise():
    while True:
        async with await aioble.advertise(
                250000, # advertising interval (ms)
                name="ESP32",
                services=[_COMM_UUID],
        ) as connection:
            print(f"Connection from {connection.device}")
            await write(connection)
            await connection.disconnected(timeout_ms=None) # may need timeout later

async def main():
    asyncio.run(advertise())

asyncio.run(main())
