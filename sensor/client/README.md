# Overview
The peripheral device has been tested with an *ESP32 DevKitc V4*, is writen in [MicroPython](https://micropython.org/download/), and is designed to run on [bare metal](https://www.techopedia.com/definition/2153/bare-metal). The code makes use of its `bluetooth` and `uasyncio` libraries. The code also relies on 
* [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble), an asynchronous wrapper for MicroPython's `ubluetooth` API.
* a modified version of [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater), which allows for automatic code updates from GitHub

# Setup

## Requirements
Before proceding, make sure you have the following installed:
* [VisualStudio Code](https://code.visualstudio.com/Download) or similar IDE like Arduino
	* [PlatformIO Extension](https://randomnerdtutorials.com/vs-code-platformio-ide-esp32-esp8266-arduino/#2)
	* [Pymakr Extension](https://lemariva.com/blog/2018/12/micropython-visual-studio-code-as-ide#:~:text=Code%20%2D%20Pymakr%20extension-,To,-use%20VSCode%20for)
		* [Node.js](https://nodejs.org/en/)
## How to use
To start, plug the microcontroller in and open VScode. Type `ctrl + shift+ p` and select the `Get Started: Open Walkthrough... > Pymakr 2 - Getting Started` option. Follow the `Connect a Device` tutorial to gain access to the microcontroller. To run files:
1. Download this repo to your local device.
2. Create a new project using the pymakr window, selecting the root folder as `../hfs.main/sensor/client` (make sure you don't select any of the default package options, ALL of them will erase `boot.py` and `main.py`.
3. Enable `dev-mode` for the project in the pymakr window (optional).
4. Click the sync project to device button to upload and run your file (not required if `dev-mode` is enabled).


> ### Common Issues
> So many things go wrong, and if they do, this is the place for you.
> ##### OSError: 16
> This error is a generic `resource is busy` error. To resolve it, try hard resetting the device in VS Code. You will probably have to do this everytime you press `ctrl + c` to stop the program.

On boot, the device will automatically load the `boot.py` then `main.py` files. On boot, `main.py` will begin scanning for peripherals and connect to them if everything works. Sometimes if the py cache does nor recompile automatically, this will have to be done manually by calling import main or import boot using the terminal. Currently, programs are halted via `ctrl + c`.

# To-do
* Create an install script for the microcontroller code
