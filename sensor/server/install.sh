#!/bin/bash

echo "Installing required server files..."

curl -sL "https://deb.nodesource.com/setup_16.x" | sudo bash -

echo "[Desktop Entry]" > $file
echo "Exec=sudo python3 /home/biosense1/hfs.main/sensor/server/bt-central.py" >> $file
echo "Exec=sudo node /home/biosense1/hfs.main/sensor/server/server.js" >> $file
#echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo python3 /home/biosense1/hfs.main/server/bt-central.py; /bin/bash'\"" >> $file
#echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo node /home/biosense1/hfs.main/server/server.js; /bin/bash'\"" >> $file

echo "Install completed, reboot now."