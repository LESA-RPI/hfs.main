print("Initializing...")
from bleak import BleakClient, BleakScanner, BleakError
import json
from math import pi

import time
import struct
import asyncio
from datetime import datetime

import graphing

# load the configurations
_CONFIG = None
_AVERAGE_FLUX = 1

# initialize the addresses and uuids
_ADDRESSES = {"A8:03:2A:6A:36:E6", "B8:27:EB:F1:28:DD"}
_HANDLES = set() 

_COMM_UUID = "26c00001-ece0-4f7a-b663-223de05387cc"
_COMM_RW_UUID = "26c00002-ece0-4f7a-b663-223de05387cc"

def load_config():
    global _CONFIG, _AVERAGE_FLUX
    # load the config file
    with open("/usr/local/src/hfs/config.json", "r") as file:
        _CONFIG = json.load(file)
    # compute the average flux
    sensing_area = ((_CONFIG["constants"]["cutoff_diameter_mm"] / 2) ** 2) * pi
    _AVERAGE_FLUX = _CONFIG["constants"]["total_canopy_flux"] / sensing_area
    

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
    decoded_data = struct.unpack("<iii", data)
    return (decoded_data[0], decoded_data[1] / 100, decoded_data[2])

def scan_handler(device, data):
    print(f"Found '{device.address}'")
    print_ad_data(data)

def notification_handler(sender, data):
    # decode the data and print to logs
    chlf_raw, distance_mm, timestamp = decode(data)
    print(f"{sender}: {timestamp} {chlf_raw} {distance_mm}")
    # compute the datetime, sensor id, normal chlf, and chlf factor
    dt_timestamp = datetime.fromtimestamp(timestamp)
    chlf_factor = (chlf_raw * _CONFIG["constants"]["k"]) / (_AVERAGE_FLUX * _AVERAGE_FLUX * distance_mm * distance_mm)
    chlf_normal = chlf_raw / _CONFIG["constants"]["max_raw_value"]
    sensor_id = 0 # todo
    # update the local visuals
    graphing.update(dt_timestamp, sensor_id, chlf_raw, chlf_normal, chlf_factor)
    # update the database
    # todo

def disconnect_handler(client):
    print(f"Disconnected from {client.address}")

async def scan(timeout=5.0):
    scanner = BleakScanner(detection_callback=scan_handler)

    print("Starting scan...")
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()
    print("Scan finished.")

    return list( filter(address_filter, scanner.discovered_devices) )

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
    print("Loading config.json...")
    await load_config()

    found_device = False
    while not found_device:
        devices = await scan()
        if devices:
            print("Found device(s).")
            found_device = True
        else:
            print("No devices found. Retrying in 10 seconds..")
            time.sleep(10)

    await asyncio.gather(*(connect_to_device(dev) for dev in devices))

if __name__ == "__main__":
    asyncio.run(main())
