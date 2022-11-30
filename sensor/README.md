# Horticulture Fluorescence Sensor Project
This code facilitates multi-point Bluetooth connections between a central device and peripheral devices.

# Requirements
Microcontrollers must have Bluetooth capability.

## Central device
The central device has been tested with a *Raspberry Pi Zero W*.

To install or update the HFS library in `/usr/local/src/`, run the following command: 

```
wget -O hfs.zip "https://github.com/LESA-RPI/hfs.main/archive/refs/heads/main.zip" && sudo unzip -o -j hfs.zip 'hfs.*/sensor/server/*' -d /usr/local/src/hfs/ && rm hfs.zip
```

Then to build the server dependencies and begin server setup, run:

```
sudo sh /usr/local/src/hfs/install.sh
```

To start the server, simply reboot the PI and both the webpage and bluetooth capabilities will automatically launch.

## Peripheral device
The peripheral device has been tested with an *ESP32 DevKitc V4* and is designed to run on [bare metal](https://www.techopedia.com/definition/2153/bare-metal).

The peripheral code is written in [MicroPython](https://micropython.org/download/) and makes use of its `bluetooth` and `uasyncio` libraries. The code also relies on [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble), an asynchronous wrapper for MicroPython's `ubluetooth` API.

# How to use
Activate the peripheral(s). There are many ways to do this depending on what microcontroller you use; consult the manual if needed. For the ESP32, the code can be manually run by importing `client/bt-peripheral.py` in the MicroPython REPL.

After this, we can activate the central device via `python3 server/bt-central.py`. The central device code will begin scanning for peripherals and connect to them if everything works.

Currently, programs are halted via `Ctrl+C`.

# To-do
- This section
