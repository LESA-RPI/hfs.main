#!/bin/bash

echo "Installing required server files..."

curl -sL "https://deb.nodesource.com/setup_10.x" | sudo bash -
node --version

file="/etc/xdg/autostart/myapp.desktop"

echo "[Desktop Entry]" > $file
echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo python3 /home/pi/server/bt-central.py; /bin/bash'\"" >> $file
echo "Exec=lxterminal --command=\"/bin/bash -c 'sudo node /home/pi/server/server.js; /bin/bash'\"" >> $file
echo "Exec=chromium-browser http://127.0.0.1:3000/" >> $file

echo "Install completed."