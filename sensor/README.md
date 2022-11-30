# Horticulture Fluorescence Sensor Project
This code facilitates multi-point Bluetooth connections between a central device and peripheral devices.

# Requirements
Microcontrollers must have Bluetooth capability.

## Central device
The central device has been tested with a *Raspberry Pi Zero W*.

> ### Connectivity Issues
> For whatever reason, RPIs dislike setting themselves up properly. Before continuing, make sure you can `ping google.com` sucessfully. If something seems off, try the following solutions:
> ##### Improper Hostname
> Make sure your hostname has been properly changed, especially if this is a newly installed PI. Type in `sudo vi /ect/hosts` and make sure that the line starting with `127.0.1.1` has the proper hostname [(source)](https://raspberrypi.stackexchange.com/questions/92751/temporary-failure-in-name-resolution).
> ##### DNS Resolution
> Sometimes the default DNS servers are just bad. Run the command `echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf.head` to add google.com to the list of nameservers to use [(source)](https://raspberrypi.stackexchange.com/questions/64556/problem-with-dns).

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
