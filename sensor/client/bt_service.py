# Bluetooth peripheral code for fluorescence sensor 

import aioble
import uasyncio as asyncio
import bluetooth as bt
import struct
from machine import Pin, ADC

import bt_programs

# UUID constants
_COMM_UUID = bt.UUID("26c00001-ece0-4f7a-b663-223de05387cc")
_COMM_RW_UUID = bt.UUID("26c00002-ece0-4f7a-b663-223de05387cc")

_RUN = 0
_GET = 1
_SET = 2

_TIMEOUT_MS = 5000

# globals
FUNCTION = bt_programs.DEFAULT

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


async def isDisconnected(connection):
    try:
        await connection.disconnected(timeout_ms=_TIMEOUT_MS)
        print(connection)
        print(connection.__dict__)
        return True
    except (asyncio.TimeoutError, asyncio.CancelledError):
        return False

async def _start():
    # continuously advertise
    print("test1")
    while True:
        # wait for the server to find us
        print("test2")
        connection = await aioble.advertise(
                250000, # advertising interval (ms)
                name="ESP32 - HFS",
                services=[_COMM_UUID],
        )
        print(f"Connection from {connection.device}")

        while True:
            try: 
                # wait for the server to tell us to do something
                print("test3")
                
                await comm_characteristic.written(timeout_ms=_TIMEOUT_MS)
                cmd, data = struct.unpack("HH", comm_characteristic.read())
                print("cmd: ", comm_characteristic.read())
                # req will either a command to run the current function, change it, or request a list of valid functions
                if cmd == _RUN:
                    FUNCTION(connection, comm_characteristic, data)
                elif cmd == _GET:
                    bt_programs.get(connection, comm_characteristic)
                elif cmd == _SET:
                    bt_programs.setDefault(connection, comm_characteristic, data)
                
                #comm_characteristic.write("periph1")
                #comm_characteristic.notify(connection)

            except asyncio.TimeoutError:
                print("test4")
                # check to see if we have been disconnected
                if await isDisconnected(connection):
                    break

def start():
    asyncio.run(_start())

if __name__ == "__main__":
    start()