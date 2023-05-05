# Bluetooth peripheral code for fluorescence sensor 

import aioble
import uasyncio as asyncio
import bluetooth as bt
import struct
from machine import Pin, ADC, RTC

import bt_programs
import device_sensor as device
# UUID constants
_COMM_UUID = bt.UUID("26c00001-ece0-4f7a-b663-223de05387cc")
_COMM_RW_UUID = bt.UUID("26c00002-ece0-4f7a-b663-223de05387cc")

_RUN = 0
_GET = 1
_SET = 2
_RUN_DEFAULT = 4
_UPDATE = 5
_SETTIME = 6

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


async def _start():
    # continuously advertise
    while True:
        # wait for the server to find us
        print("[INFO] Waiting for incoming connection")
        connection = await aioble.advertise(
                250000, # advertising interval (ms)
                name="ESP32_HFS",
                services=[_COMM_UUID],
        )
        device.log(connection, comm_characteristic, f"[INFO] Connected to {connection.device}")
        device.log(connection, comm_characteristic, f"[INFO] This device is running v{device.CURRENT_VERSION}")
        while True:
            try: 
                # wait for the server to tell us to do something
                device.log(connection, comm_characteristic, "[INFO] Waiting for command...")
                await comm_characteristic.written(timeout_ms=_TIMEOUT_MS)
                cmd, data, sampleSize, frequency = 0, None, 0, 0
                try:
                    cmd, data, sampleSize, frequency = struct.unpack("HILL", comm_characteristic.read())
                except Exception as error:
                    device.log(connection, comm_characteristic, f"[ERROR] Could not parse command")
                    continue
                device.log(connection, comm_characteristic, f"[INFO] Recieved command {str(cmd)} with parameter {str(data)}")
                # req will either a command to run the current function, change it, or request a list of valid functions
                if cmd == _RUN_DEFAULT:
                    await FUNCTION(connection, comm_characteristic, frequency, sampleSize)
                elif cmd == _GET:
                    bt_programs.get(connection, comm_characteristic)
                elif cmd == _SET:
                    bt_programs.setDefault(connection, comm_characteristic, frequency, sampleSize)
                elif cmd == _RUN:
                    func = bt_programs.lookup(data)
                    await func(connection, comm_characteristic, frequency, sampleSize)
                elif cmd == _UPDATE:
                    device.log(connection, comm_characteristic, "Disconnecting to update device, see you soon!")
                    await aioble.disconnect()
                    import git_update
                    git_update.update()
                elif cmd == _SETTIME:
                    import time
                    device.log(connection, comm_characteristic, f"[INFO] Changing internal time to {str(time.gmtime(int(data)))}")
                    RTC().datetime(time.gmtime(int(data)))
                    
                #comm_characteristic.write("periph1")
                #comm_characteristic.notify(connection)

            except asyncio.TimeoutError:
                # check to see if we have been disconnected
                if not connection.is_connected():
                    print("[WARNING] Disconnected!")
                    break

def start():
    asyncio.run(_start())

if __name__ == "__main__":
    start()