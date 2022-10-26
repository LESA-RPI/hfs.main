from bleak import BleakClient, BleakScanner, BleakError

import struct
import asyncio
from datetime import datetime

import graphing

_ADDRESSES = {"A8:03:2A:6A:36:E6", "B8:27:EB:F1:28:DD"}
_HANDLES = set() 

_COMM_UUID = "26c00001-ece0-4f7a-b663-223de05387cc"
_COMM_RW_UUID = "26c00002-ece0-4f7a-b663-223de05387cc"

def address_filter(x):
    return x.address in _ADDRESSES

# helper to print advertisement data
def print_ad_data(data):
    if data.local_name:
        print(f"\tName: {data.local_name}")
    if data.service_uuids:
        print("\tServices:")
        for service in data.service_uuids:
            print(f"\t- {service}")

# decode value from characteristic
def decode(data):
    return struct.unpack("<h", data)[0] / 100

def scan_handler(device, data):
    print(f"Found '{device.address}'")
    print_ad_data(data)

def notification_handler(sender, data):
    decoded_data = decode(data)
    print(f"{sender}: {decoded_data}")
    # update the visuals
    temp_timestamp = datetime.now()
    graphs.update(temp_timestamp, 0, float(decoded_data) * 4095, float(decoded_data) * 100, 0.2)

def disconnect_handler(client):
    print(f"Disconnected from {client.address}")

async def scan(timeout=5.0):
    scanner = BleakScanner(detection_callback=scan_handler)

    print("Starting scan...")
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()
    print("Scan finished.")

    return filter(address_filter, scanner.discovered_devices)

async def connect_to_device(device):
    print(f"Connecting to {device}...")
    async with BleakClient(
        device, timeout=5.0, disconnected_callback=disconnect_handler
    ) as client:
        print(f"Connected to {client.address}")
        try:
            await client.start_notify(_COMM_RW_UUID, notification_handler)
            while True:
                try:
                    await asyncio.sleep(0.5)
                except KeyboardInterrupt:
                    print("shutting down central...")
                    return
        except BleakError:
            print(f"{client.address} does not contain necessary characteristic")

async def main():
    devices = await scan()
    await asyncio.gather(*(connect_to_device(dev) for dev in devices))

if __name__ == "__main__":
    asyncio.run(main())
