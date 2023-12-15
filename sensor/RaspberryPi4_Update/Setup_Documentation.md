# Installing esptool.py on Your Computer

## Step 1: Install Python
First, ensure you have Python installed on your system. You can use either Python 2.7, Python 3.4, or a newer version. We recommend Python 3.7.X for the best experience. Download and install it from [Python's official website](https://www.python.org/).

## Step 2: Install esptool.py Using pip
With Python 3 installed, follow these steps:
1. Open a Terminal window.
2. Install the latest stable release of esptool.py using pip:

    pip3 install esptool

**Note**: In some cases, this command may not work and you might receive an error. If this happens, try the following alternative commands:
- `pip install esptool`
- `python -m pip install esptool`
- `pip2 install esptool`

## Step 3: Install Setuptools
Setuptools is a requirement for esptool.py but it might not be available on all systems by default. You can install it using:

    pip3 install setuptools


## Step 4: Verify Installation
After installing, esptool.py will be installed in the default Python executables directory. To verify that esptool.py is correctly installed, run the following command in your Terminal:

    python -m esptool

This should execute esptool.py, confirming that the installation was successful.

# Flashing ESP32 with MicroPython

### Main Link: 
https://micropython.org/download/ESP32_GENERIC/

The following files are firmware that should work on most ESP32-based boards with 4MiB of flash, including WROOM WROVER, SOLO, PICO, and MINI modules.

Board used for this test: ESP32-VROVER

MicroPython Version for this test: v1.21.0 (2023-10-05)

### Steps: 

https://github.com/espressif/esptool

MicroPython recommends the use of esptool.py to program the ESP32.

Another dependency required for this is:

    pip3 install intelhex

### Ensure that the micro USB cable connected to the ESP32 is high quality and has data wiring, not just power. 
If the wire seems thin, it most likely is inadequate for the job. 

### Next, run the following sequences to clear the board and install MicroPython

    python -m esptool erase_flash

(Depending on the board, the "boot" button may need to be held down while running the above code for a successful erase_flash)

### Now, flash MicroPython to the ESP32

    python -m esptool --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-SPIRAM-20231005-v1.21.0.bin

(last portion will be different depending on version, also ensure to cd to correct directory)

### Official Espressif Troubleshooting Documentation
https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html

### Connecting the ESP32 to WiFi

Script named as main.py to automatically run on boot. 

Functioning script is included in the folder.

SSID: ArpaE
PASSWORD: ArpaE2019

### Installing "urequests" MicroPython Dependency

Using Thonny, go to Tools --> Manage Packages --> Search for 'urequests' --> install on ESP32

Version used: 0.8.0