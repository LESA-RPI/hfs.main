#!/bin/bash

echo "Installing required server packages and files..."

# create a public directory and move the index file into it
mkdir -v "/usr/local/src/hfs/public"
mv -v "/usr/local/src/hfs/index.html" "/usr/local/src/hfs/public/index.html" 

# install Node.js v16 from the unoffical arm6l release following this https://gist.github.com/davps/6c6e0ba59d023a9e3963cea4ad0fb516 guide
wget -P /usr/local https://unofficial-builds.nodejs.org/download/release/v16.9.1/node-v16.9.1-linux-armv6l.tar.gz
tar -xvzf /usr/local/node-v16.9.1-linux-armv6l.tar.gz -C /usr/local
rm -rvf /usr/local/node-v16.9.1-linux-armv6l.tar.gz
cp -Rv /usr/local/node-v16.9.1-linux-armv6l/bin /usr/
cp -Rv /usr/local/node-v16.9.1-linux-armv6l/lib /usr/
cp -Rv /usr/local/node-v16.9.1-linux-armv6l/include /usr/
cp -Rv /usr/local/node-v16.9.1-linux-armv6l/share /usr/

rm -rvf /usr/local/node-v16.9.1-linux-armv6l
node -v
npm -v

# install all requirements for the Bluetooth connectivity
pip3 install bleak==0.14.* --force-reinstall -vvv

# install all requirements for local webserver
# NOTE: compatible numpy versions can be found here https://github.com/matplotlib/matplotlib/blob/ac3d0caf0007389579a5fa2576d95657b03d3f02/doc/devel/min_dep_policy.rst#id1
pip3 install matplotlib==3.6.* --force-reinstall -vvv
python3 -c "import matplotlib"

# requirements for the database management
pip3 install psycopg2==2.9.* --force-reinstall -vvv
apt-get install postgresql-14

# this is often missing on Raspberry Pi and is required for numpy
apt-get install libatlas-base-dev

# make the Bluetooth application
echo "[Unit]\nDescription=The Bluetooth service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/python3 /usr/local/src/hfs/bt-central.py\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-bluetooth.service"

# make the local Webserver application
echo "[Unit]\nDescription=The local site service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/node /usr/local/src/hfs/server.js\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-local.service"

echo "Install completed, please reboot to launch the server."
