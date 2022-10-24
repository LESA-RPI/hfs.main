#!/bin/bash

echo "Installing required server packages and files..."

# install Node.js v16 from the unoffical arm6l release following this https://gist.github.com/davps/6c6e0ba59d023a9e3963cea4ad0fb516 guide
wget https://unofficial-builds.nodejs.org/download/release/v16.9.1/node-v16.9.1-linux-armv6l.tar.gz -P /usr/local
tar -xzf /usr/local/node-v16.9.1-linux-armv6l.tar.gz
sudo rm -rf /usr/local/node-v16.9.1-linux-armv6l.tar.gz
sudo cp -R /usr/local/node-v16.9.1-linux-armv6l/* /usr/local
sudo rm -rf /usr/local/node-v16.9.1-linux-armv6l
node -v
npm -v

# install all requirements for the Bluetooth connectivity
pip3 install bleak==0.14.* --force-reinstall

# install all requirements for local webserver
# NOTE: Minimum NUMPY versions can be found here https://github.com/matplotlib/matplotlib/blob/ac3d0caf0007389579a5fa2576d95657b03d3f02/doc/devel/min_dep_policy.rst#id1
pip3 install numpy==1.23.* --force-reinstall
pip3 install matplotlib==3.6.* --force-reinstall

# this is often missing on Raspberry Pi
sudo apt-get install libatlas-base-dev

# make the Bluetooth application
echo "[Unit]\nDescription=The Bluetooth service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/python3 /usr/local/src/hfs.main/sensor/server/bt-central.py\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-bluetooth.service"

# make the local Webserver application
echo "[Unit]\nDescription=The Bluetooth service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/node /usr/local/src/hfs.main/sensor/server/server.js\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-local.service"

echo "Install completed, please reboot to launch the server."
