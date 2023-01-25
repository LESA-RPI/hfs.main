#!/bin/bash

RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# add the google nameserver (temporarilly) because it isn't there half the time
sudo sh -c "echo nameserver 192.168.1.1'\n'nameserver 8.8.8.8 > /etc/resolv.conf"

echo "${BLUE}INFO: installing required server packages and files...${NC}"
echo "${YELLOW}WARNING: installation can take upwards of an hour on a new build as node16.9.1 must be rebuilt from the source!${NC}"
echo "${YELLOW}WARNING: it is reccomended that you use screen to run this command${NC}"
echo "${BLUE}INFO: this installation is only for developers and rebuilds all required packages from scratch${NC}"

# Increase the number of retries
echo 'Acquire::Retries "50";' > "/etc/apt/apt.conf.d/80-retries"

# Make the app directory
mkdir -v "/usr/local/src/hfs/public"

# install the required apt packages
sudo apt update
sudo apt upgrade -y
sudo apt install wget -y
sudo apt install ca-certificates -y
sudo apt install software-properties-common -y # need add-apt-repository
sudo apt install libatlas-base-dev -y # this is often missing on Raspberry Pi and is required for numpy
sudo apt update

# install python3.9
sudo apt install python3.9
#if ! type "$python3.9" > /dev/null; then
	
	#wget "https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz"
	#sudo tar -xf Python-3.11.0.tar.xz
	#sudo ./Python-3.11.0/configure --enable-optimizations
	#sudo make altinstall
	# https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh
	# https://itheo.tech/ultimate-python-installation-on-a-raspberry-pi-and-ubuntu-script
	#sudo add-apt-repository ppa:deadsnakes/ppa -y
	#sudo apt update
	#sudo apt install python3.11 -y
	#sudo apt install python3.11-dev -y
#fi

# install pip3.9
if ! type "$pip3.9" > /dev/null; then
	wget -P "/usr/local/src/hfs" "https://bootstrap.pypa.io/get-pip.py"
	sudo python3.9 get-pip.py
	pip3.9 install --upgrade setuptools
	rm -rvf "/usr/local/src/hfs/get-pip.py"
	#export PATH=/usr/lib/postgresql/14/bin/:$PATH
	# pip install -r packageName/requrirements.txt
fi

# Move the index file to public
mv -v "/usr/local/src/hfs/index.html" "/usr/local/src/hfs/public/index.html" 

# install node
if ! type "$node" > /dev/null; then
	echo "Installing Node.js v16 from the unoffical arm6l release following this https://gist.github.com/davps/6c6e0ba59d023a9e3963cea4ad0fb516 guide"
	wget -P "/usr/local" https://unofficial-builds.nodejs.org/download/release/v16.9.1/node-v16.9.1-linux-armv6l.tar.gz
	tar -xvzf "/usr/local/node-v16.9.1-linux-armv6l.tar.gz" -C "/usr/local"
	rm -rvf "/usr/local/node-v16.9.1-linux-armv6l.tar.gz"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/bin" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/lib" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/include" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/share" "/usr/"
	rm -rvf /usr/local/node-v16.9.1-linux-armv6l
fi

echo -e "${BLUE} INFO Reinstalling project dependencies${NC}"

# install the required node packages
npm install "/usr/local/src/hfs"

# install all requirements for the Bluetooth connectivity
pip3.9 install bleak==0.14.* --force-reinstall -vvv

# install all requirements for local webserver
# NOTE: compatible numpy versions can be found here https://github.com/matplotlib/matplotlib/blob/ac3d0caf0007389579a5fa2576d95657b03d3f02/doc/devel/min_dep_policy.rst#id1
pip3.9 install matplotlib==3.6.* --force-reinstall -vvv
python3.9 -c "import matplotlib"

# install psql
if ! type "$psql" > /dev/null; then
	# requirements for the database management
	wget --quiet -O - "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | sudo apt-key add -
	sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
	sudo apt update
	sudo apt install postgresql-13
	sudo sed -i 's/local   all             postgres                                peer/local   all             postgres                                trust/' '/etc/postgresql/14/main/pg_hba.conf'
	sudo sed -i 's/local   all             all                                     peer/local   all             all                                     trust/' '/etc/postgresql/14/main/pg_hba.conf'
	sudo passwd -d postgres
	sudo systemctl restart postgresql
	sudo systemctl enable postgresql
	sudo psql -U postgres -c "ALTER USER postgres PASSWORD 'admin';"
	su - postgres -c 'psql -c "CREATE TABLE IF NOT EXISTS data (id int, timestamp timestamp, chlf_raw int, chlf_normal real, f_factor real, distance real);"'
fi

# make the Bluetooth application
echo "[Unit]\nDescription=The Bluetooth service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/python3.11 /usr/local/src/hfs/bt-central.py\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-bluetooth.service"

# make the local Webserver application
echo "[Unit]\nDescription=The local site service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/node /usr/local/src/hfs/server.js\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-local.service"

# cleanup
sudo apt autoremove -y

# reset the number of retries
echo 'Acquire::Retries "3";' > "/etc/apt/apt.conf.d/80-retries"

# verify installation
python3.9 -V
pip3.9 -V
node -v
output=$(node -v)
if [ "$output" != "v16.9.1" ]; then
    echo -e "${RED}ERROR: build failed, node ${output} is installed instead of node v16.9.1${NC}"
	return 1
fi
npm -v
sudo systemctl status postgresql
su - postgres -c 'psql -c "TABLE data"'

echo -e "${BLUE}Install completed, please reboot to launch the server.${NC}"
