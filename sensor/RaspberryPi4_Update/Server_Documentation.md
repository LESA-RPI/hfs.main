# Server Documentation

This is a comprehensive server documentation for the Raspberry Pi 4 in connection to the ESP32. All packages and versions are up to date as of 12/14/2023.

### Pi Setup and Internet Connection

Raspberry Pi Hostname: hfsserver
Raspberry Pi Password: password
Version used: Debian GNU / Linux 12 (bookworm)

Check version:
    cat /etc/os-release

Connect the Raspberry Pi to the same internet as the ESP32:
SSID: ArpaE
PASSWORD: ArpaE2019

### Installing Python and Dependencies

The following lines of code will install all the necessary applications and dependencies for this project.

    sudo apt install python3 python3-pip

    sudo apt install python3-flask

    sudo apt install sqlite3

Flask version: 2.2.2

### Basic Server Setup to Send over WiFi

Install UFW Firewall Tool (to whitelist ESP32 IP)

    sudo apt install ufw

Whitelist ESP32 IP

    sudo ufw allow in from 192.168.1.49 to any port 5000
    sudo ufw enable

IP address and port number will change depending on the system setup.

### Setup the Database in SQLite3

This is very much dependent upon the necessary requirements and desired schema of the data being collected. 

For testing purposes, a simple schema was created to record the timestamp at button press for the ESP32.

SQLite3 documentation is found here: https://www.sqlite.org/docs.html

Flask on the Raspberry Pi also needs permissions to access the Database created. 

Permissions can be read by navigating to the main webapp folder via terminal and typing:
    ls -l

Write permission can be granted to Flask by using:
    sudo chmod 644 nameofdatabasefile.db

All final code used for testing can be found in the GitHub folders included in the repository.

The past iterations are also kept for debugging purposes. 

### Latest / Current Versions

Latest test versions are: 
- templates folder
- app.py file
- timestamps.db file

### Final Results (end of semester, not fully functional but providing as much documentation as possible)

- The pushed button does successfully send to the Raspberry Pi 4 over WiFi, and functions as intended

- The basic Flask server functions as intended.

- The SQLite database does not function as intended. I believe the issues concern local permissions. 

- I attempted to work on a reverse button push, where the ESP32 could be triggered via web interface, but I did not have time to complete this task. 

### Additional Documentation from Official Websites

Flask documentation: https://flask.palletsprojects.com/
SQLite3 documentation: https://www.sqlite.org/docs.html
Micropython Wi-Fi library: https://docs.micropython.org/en/latest/library/network.WLAN.html
Micropython urequests library: https://docs.micropython.org/en/latest/library/esp32.html
MicroPython Button library: https://docs.micropython.org/en/latest/pyboard/tutorial/switch.html
