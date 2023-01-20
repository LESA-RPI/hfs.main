
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

# encode data to characteristic
def encode(data):
    return struct.pack("<h", int(data * 100))

# write to characteristic
async def write(conn):
    # slight delay to avoid multi-connection issues
    #await asyncio.sleep(3.0)

    t = 50
    while True:
        t += random.uniform(-0.5, 0.5)
        print(f"Writing '{t}' to peripheral...")
        comm_characteristic.write( encode(t) )
        comm_characteristic.notify(conn)
        await asyncio.sleep_ms(500)

# advertise services
async def advertise():
    while True:
        async with await aioble.advertise(
                250000, # advertising interval (ms)
                name="ESP32",
                services=[_COMM_UUID],
        ) as connection:
            print(f"Connection from {connection.device}")
            await write(connection)
            await connection.disconnected(timeout_ms=None)

async def main():
    asyncio.run( advertise() )

asyncio.run(main())
