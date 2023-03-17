import logging
from logging.handlers import RotatingFileHandler
# Load the logfile
log_name = "/usr/local/src/hfs/public/public.log"
#log_name = "./public/public.log"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = RotatingFileHandler(log_name, maxBytes= 5 * 1024, backupCount=1, encoding=None, delay=0)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', '%d/%m/%Y %H:%M:%S'))

log.addHandler(handler)

log.info('HFS server starting...')

from bleak import BleakClient, BleakScanner, BleakError
import json
from math import pi
import subprocess
import time
import struct
import asyncio
import json
from datetime import datetime
import dynamic_graphs as dgraphing
import sys

class OnMessageEvent():
  def __init__(self):
    self.listeners = {}

  async def emit(self, msg_json):
    log.info(0)
    for device_address in DEVICES.keys():
        if device_address != msg_json['addr']: continue
        await asyncio.create_task(device.onMessage(msg))

# load the configurations
_CONFIG = None
_AVERAGE_FLUX = 1

# global device list
DEVICES = dict()

class Device():
    def __init__(self, client):
        self.client = client
        self.address = self.client.address
        self.event = asyncio.Event()
        self.msg = None
        self.task = None
        self.main = None
        self.command = (0, 0)
        
    async def run(self, client, delay_min):
        while True:
            await asyncio.sleep(delay_min * 60)
            self.send(client, self.command)
    
    def send(client, command):
        client.write_gatt_char(_COMM_RW_UUID, data=struct.pack("HH", *command))
    
    def disconnect(self):
        if (self.task != None) and (not self.task.cancelled()):
            self.task.cancel()
        self.main.cancel()
    
    async def onMessage(self, msg):
        self.msg = msg
        self.event.set()
    
    def handler(self, client, cmd, data):
        if cmd < 0: # send the command directly to the controller
            self.send(client, (abs(cmd), data))
        elif cmd == 2: # update the command we run
            self.command = (abs(data), self.command[1])
        elif cmd == 4: # update the delay in our run function
            if (self.task != None) and (not self.task.cancelled()):
                self.task.cancel()
            self.task = asyncio.create_task(self.run(client, data))
        else:
            log.warning(f'Unknown command {self.msg["cmd"]}')
                        
    async def keep_alive(self): 
        async with BleakClient(
            self.client, timeout=5.0, disconnected_callback=disconnect_handler
        ) as client:
            log.info(f"Connected to {client.address}")
            try:
                await client.start_notify(_COMM_RW_UUID, notification_handler)
                while True:
                    await self.event.wait() # wait for us to recieve a message
                    self.handler(client, self.msg['cmd'], self.msg['data']) # handle the message
                    self.event.clear() # reset the message flag

            except (BleakError, KeyboardInterrupt):
                log.info(f"{client.address} disconnected")
                pass
    

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
    
#load_config()
#notification_handler('dummy', struct.pack('<HIHH', 0, int(time.time()), int(15.30 * 100), 3207))



async def scan(timeout=5.0):
    scanner = BleakScanner(detection_callback=scan_handler, service_uuids=_SERVICE_UUIDS)

    log.info('Starting scan...')
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()
    log.info('Scan finished.')

    #return scanner.discovered_devices
    try:
        return await scanner.get_discovered_devices()
    except Exception as exception:
        log.error(exception)
        return []
        
def disconnect_handler(client):
    log.info(f"Disconnected from {client.address}")
    device = DEVICES[client.address]
    DEVICES.pop(client.address)
    device.disconnect()

async def connect_to_device(client):
    if client.address in DEVICES: return
    log.info(f'Connecting to {client}.')
    device = Device(client)
    DEVICES[client.address] = device
    device.main = device.keep_alive()

async def ainput():
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

async def inputLoop():
    global on_msg_event
    run = True
    while run:
        try:
            msg = json.loads(await ainput())
            log.info(f'> {msg}')
            if msg['cmd'] == 3: # wants a list of returned devices
                devices = []
                log.info(DEVICES)
                for device in DEVICES.values():
                    log.info(device.client)
                    devices.append(json.dumps(device.client.__dict__))
                response = json.dumps({'code': 1, 'devices': devices})
                log.info(f'< {response}')
                print(response)
            else:                
                try:
                    await on_msg_event.emit(msg)
                    log.info("< {'code': 1}")
                    print(json.dumps({'code': 1}))
                except Exception as error:
                    log.info(f"< \{'code': 0, 'error': {error}\}")
                    print(json.dumps({'code': 0, 'error': error}))
                    
                
        except EOFError:
            log.warning("EOF Error")
            print(json.dumps({'code': 0})) # tell the Node.js server we crashed
            run = False

async def bleLoop():
    run = True
    while run:
        devices = await scan()
        if devices:
            log.info("Found device(s) with valid service.")
            asyncio.gather(*(connect_to_device(dev) for dev in devices))
            log.info(devices)
            log.info("Searching for devices again in 5 minutes..")
            await asyncio.sleep(60*5)
        else:
            log.info("No devices with valid services found. Retrying in 10 seconds..")
            await asyncio.sleep(10)

on_msg_event = OnMessageEvent()

async def main():
    log.info("Loading config.json...")
    
    if not load_config():
        log.warning("Loading expected config.json failed, resorting to local configuration")
        load_config("./config.json")

    task_ble = asyncio.create_task(bleLoop())
    task_api = asyncio.create_task(inputLoop())
    
    await task_ble
    log.error("BLE task has ended prematurely!")
    await task_api
    log.error("API task has ended prematurely!")

if __name__ == "__main__":
    asyncio.run(main())
