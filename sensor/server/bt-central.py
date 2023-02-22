from bleak import BleakClient, BleakScanner, BleakError
import json
from math import pi
import subprocess
import time
import struct
import asyncio
from datetime import datetime
import dynamic_graphs as dgraphing
import logging
from logging.handlers import RotatingFileHandler

# Load the logfile
log_name = "/usr/local/src/hfs/public/public.log"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = RotatingFileHandler(log_name, maxBytes=5 * 5 * 1024, backupCount=0, encoding=None, delay=0)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', '%d/%m/%Y %H:%M:%S'))

log.addHandler(handler)

log.info('HFS server starting...')

# load the configurations
_CONFIG = None
_AVERAGE_FLUX = 1

# initialize the addresses and uuids
_ADDRESSES = {"A8:03:2A:6A:36:E6", "B8:27:EB:F1:28:DD"}
_HANDLES = set()

_COMM_UUID = "26c00001-ece0-4f7a-b663-223de05387cc"
_COMM_RW_UUID = "26c00002-ece0-4f7a-b663-223de05387cc"

_SERVICE_UUIDS = [_COMM_UUID]

def load_config(path="/usr/local/src/hfs/config.json"):
    global _CONFIG, _AVERAGE_FLUX
    # load the config file
    try:
        with open(path, "r") as file:
            _CONFIG = json.load(file)
        # compute the average flux
        sensing_area = ((_CONFIG["constants"]["cutoff_diameter_mm"] / 2) ** 2) * pi
        _AVERAGE_FLUX = _CONFIG["constants"]["total_canopy_flux"] / sensing_area
        return True
    except:
        log.warning(f"{path} not found")
        return False

def address_filter(x):
    if not x.service_uuids:
        return False
    for service in data.service_uuids:
        if service == _COMM_UUID:
            return True
    return False

# helper to print advertisement data
def print_ad_data(data):
    count = 0
    if data.service_uuids:
        for service in data.service_uuids:
            count += 1
    if data.local_name:
        log.info(f"Found '{data.local_name}' with {count} services")
        return
    log.info(f"Found '{device.address}' with {count} services")

# decode value from characteristic
def decode(data):
    decoded_data = struct.unpack("<HIHH", data)
    return (decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3])

def scan_handler(device, data):
    print_ad_data(data)

def notification_handler(sender, data):
    # decode the data and print to logs
    id, timestamp, distance_mm, chlf_raw  = decode(data)
    log.info(f"Recieved data from {sender} (id={id}) at {timestamp}: chlf={chlf_raw} d={distance_mm}mm")
    # compute the datetime, sensor id, normal chlf, and chlf factor
    dt_timestamp = datetime.fromtimestamp(timestamp)
    f_factor = (chlf_raw * _CONFIG["constants"]["k"]) / (_AVERAGE_FLUX * _AVERAGE_FLUX * distance_mm * distance_mm)
    chlf_normal = chlf_raw / _CONFIG["constants"]["max_raw_value"]
    # update the local visuals
    dgraphing.update(dt_timestamp, id, chlf_raw, chlf_normal, f_factor)
    # update the database
    cmd = f'psql -c  "INSERT INTO data (id, timestamp, chlf_raw, chlf_normal, f_factor, distance) VALUES ({id}, to_timestamp({timestamp}), {chlf_raw}, {chlf_normal}, {f_factor}, {distance_mm});"'
    subprocess.run(["su", "-", "postgres", "-c", f"{cmd}"])
    
load_config()
notification_handler('dummy', struct.pack('<iiii', 0, int(time.time()), int(15.30 * 100), 3207))

def disconnect_handler(client):
    log.info(f"Disconnected from {client.address}")
    pass

async def scan(timeout=5.0):
    scanner = BleakScanner(detection_callback=scan_handler, service_uuids=_SERVICE_UUIDS)

    log.info('Starting scan...')
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()
    log.info('Scan finished.')

    return scanner.discovered_devices
    # return list( filter(address_filter, scanner.discovered_devices) )

async def connect_to_device(device):
    log.info(f'Connecting to {device}.')
    async with BleakClient(
        device, timeout=5.0, disconnected_callback=disconnect_handler
    ) as client:
        log.info(f"Connected to {client.address}")
        try:
            await client.start_notify(_COMM_RW_UUID, notification_handler)
            while True:
                try:
                    await asyncio.sleep(0.5)
                except KeyboardInterrupt:
                    log.info("Shutting down server...")
                    return
        except BleakError:
            log.info(f"{client.address} does not contain necessary characteristic")
            pass
            
async def main():
    log.info("Loading config.json...")
    
    if not load_config():
        log.warning("Loading expected config.json failed, resorting to local configuration")
        load_config("./config.json")

    run = True
    while run:
        devices = await scan()
        if devices:
            log.info("Found device(s) with valid service.")
            await asyncio.gather(*(connect_to_device(dev) for dev in devices))
            log.info("Searching for devices again in 5 minutes..")
            time.sleep(60*5)
        else:
            log.info("No devices with valid services found. Retrying in 10 seconds..")
            time.sleep(10)

    

if __name__ == "__main__":
    asyncio.run(main())