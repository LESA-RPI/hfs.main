# Overview
The peripheral device has been tested with an *ESP32 DevKitc V4*, is writen in [MicroPython](https://micropython.org/download/), and is designed to run on [bare metal](https://www.techopedia.com/definition/2153/bare-metal). The code makes use of its `bluetooth` and `uasyncio` libraries. The code also relies on 
* [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble), an asynchronous wrapper for MicroPython's `ubluetooth` API.
* a modified version of [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater), which allows for automatic code updates from GitHub

# Development

## Flashing Firmware
If you ever get a new microcontroller, you will need to make sure that micropython is installed on the device. First, install [esptool.py](https://github.com/espressif/esptool/) by downloading it from the source or running `pip install esptool`. Then, download the appropriate [firmware](https://micropython.org/download/esp32/). Simply follow the directions found on the download page to update firmware. 

Make sure to plug in your device and replace `ttyUSB0` with the actual serial port that the controller is plugged into. The list of ports on Linux can be found by running `ls /dev`. If you are using WSL, open your Windows Device Manager and look under the Ports category. You should see the microntontroller connected to a COM port, such as COM4. In this case, the correct path to the device should be `/dev/ttyS4`.

[[Source]](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)

## Uploading Code

Uploading code to the microcontroller will either work the first time or be the most painful experience you've had for a while. Hopefully, the VS Code method simply works for you. However, there have been issues in the past. If it doesn't work for you, don't spend too much time on it and just use the second method. 

### VS Code

Before proceding, make sure you have the following installed:
* [Node.js](https://nodejs.org/en/)
* [VisualStudio Code](https://code.visualstudio.com/Download)
	* [PlatformIO Extension](https://randomnerdtutorials.com/vs-code-platformio-ide-esp32-esp8266-arduino/#2)
	* [Pymakr Extension](https://lemariva.com/blog/2018/12/micropython-visual-studio-code-as-ide#:~:text=Code%20%2D%20Pymakr%20extension-,To,-use%20VSCode%20for)

To start, plug the microcontroller in and open VScode. Type `ctrl + shift+ p` and select the `Get Started: Open Walkthrough... > Pymakr 2 - Getting Started` option. Follow the `Connect a Device` tutorial to gain access to the microcontroller. To then run files:
1. Download this repo to your local device.
2. Open the project folder `../hfs.main/sensor/client` (you may be prompted to create a new project, which is okay, just make sure you don't select any of the default package options... ALL of them will erase `boot.py` and `main.py` which just kinda sucks).
3. Enable `dev-mode` for the project in the pymakr window (optional).
4. Click the sync project to device button to upload and run your file (not required if `dev-mode` is enabled).

> #### Common Issues
> So many things go wrong, and if they do, this is the place for you.
> ###### OSError: 16
> This error is a generic `resource is busy` error. To resolve it, try hard resetting the device in VS Code. You will probably have to do this everytime you press `ctrl + c` to stop the program.

On boot, the device will automatically load the `boot.py` then `main.py` files. On boot, `main.py` will begin scanning for peripherals and connect to them if everything works. Currently, programs are halted via `ctrl + c`.

# To-do
* Create an install script for the microcontroller code
