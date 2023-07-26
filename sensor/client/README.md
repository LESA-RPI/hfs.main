# Overview
The peripheral device has been tested with an *ESP32 DevKitc V4*(The new design uses ESP32C3Wroom), is writen in [MicroPython](https://micropython.org/download/), and is designed to run on [bare metal](https://www.techopedia.com/definition/2153/bare-metal). The code makes use of its `bluetooth` and `uasyncio` libraries. The code also relies on 
* [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble), an asynchronous wrapper for MicroPython's `ubluetooth` API.
* a modified version of [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater), which allows for automatic code updates from GitHub

# Development

## Programing with Micropython
Micropython is just a barebone version of Python. The libraries availiable to you can be found [here](https://docs.micropython.org/en/latest/library/index.html) and [here](https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/README.md#usage).

## Flashing Firmware
If you ever get a new microcontroller, you will need to make sure that micropython is installed on the device. First, install [esptool.py](https://github.com/espressif/esptool/) by downloading it from the source or running `pip install esptool`. Then, download the appropriate [firmware](https://micropython.org/download/esp32/). Simply follow the directions found on the download page to update firmware. 

Make sure to plug in your device and replace `ttyUSB0` with the actual serial port that the controller is plugged into. The list of ports on Linux can be found by running `ls /dev`. If you are using WSL, open your Windows Device Manager and look under the Ports category. You should see the microntontroller connected to a COM port, such as COM4. In this case, the correct path to the device should be `/dev/ttyS4`.

> #### Common Issues
> So many things go wrong, and if they do, this is the place for you.
> ###### [Errno 13] Permission denied
> You have the serial connected with some other program. Since only one program can access the serial port at a time, you have to disconnect the other program.
> ###### esptool: Stop Iteration
> This could be so, so many things, but first try changing the baud rate to 115200. If that doesn't work, the device may not be in boot mode. To enable boot mode, hold both the BOOT and EN, then release EN. Check out [this](https://stackoverflow.com/questions/57596413/esp32-flashing-upload-starts-and-fails-with-timeout) thread for more information.

[[Source]](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)

## Uploading Code

Uploading code to the microcontroller will either work the first time or be the most painful experience you've had for a while. Hopefully, the VS Code method simply works for you. However, there have been issues in the past. If it doesn't work for you, don't spend too much time on it and just use the second method. 

### 1) VS Code

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

### 2) Dev-Deploy
If you have found yourself here, I am very sorry. However, things can still work (kinda)! Your first goal is to access the serial prompt of the device so that you can see your debug statements. This isn't required, but really really helps in debugging and making sure things are running properly. On Linux, this can be done via the command line tool picocom (`sudo apt-get install picocom`) or minicom (`sudo apt-get install minicom`). On Windows, [TeraTerm](http://www.teraterm.org/) is reccomended. 

You can also try and access the webrepl, which is technically enabled upon boot by the device. However, [it refuses to connect over https](https://github.com/micropython/webrepl/issues/15), so that method doesn't work too well. Technically, the ESP32 is also supposed to advertise a Wi-Fi network when it doesn't connect to one, but I have found that it simply does not for whatever reason. You can find tutorials walking through these methods [here](https://www.techcoil.com/blog/how-to-setup-micropython-webrepl-on-your-esp32-development-board/) and [here](https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl), though don't have much hope for them.

Once you have a serial connection of some sort, switch over to the dev-deploy branch and follow the directions found [there](https://github.com/LESA-RPI/hfs.main/tree/dev-deploy#warning). The dev-deploy branch allows you to upload your code to GitHub and have the microcontroller automatically download the update.

There also should be some way to copy files directly over the REPL, but I haven't looked into it too much. Feel free to explore this if you dare!

[Source](https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html)

# To-do
* Create an install script for the microcontroller code
* Integrate L0 ToF into the program
