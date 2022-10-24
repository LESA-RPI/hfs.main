#!/bin/bash

echo "Installing required server packages and files..."

curl -sL "https://deb.nodesource.com/setup_16.x" | sudo bash -

pip3 install bleak==0.14.* --force-reinstall

# NOTE: Minimum NUMPY versions can be found here https://github.com/matplotlib/matplotlib/blob/ac3d0caf0007389579a5fa2576d95657b03d3f02/doc/devel/min_dep_policy.rst#id1
pip3 install numpy==1.23.* --force-reinstall
pip3 install matplotlib==3.6.* --force-reinstall

# this is often missing on Raspberry Pi
sudo apt-get install libatlas-base-dev

# add the desktop startup file application
echo "[Desktop Entry]" > $file
echo "Exec=sudo python3 /home/biosense1/hfs.main/sensor/server/bt-central.py" >> $file
echo "Exec=sudo node /home/biosense1/hfs.main/sensor/server/server.js" >> $file
#echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo python3 /home/biosense1/hfs.main/server/bt-central.py; /bin/bash'\"" >> $file
#echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo node /home/biosense1/hfs.main/server/server.js; /bin/bash'\"" >> $file

echo "Install completed, please reboot to launch the server."
