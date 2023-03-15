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

while true
do
    read -r -p 'Do you want to continue? (Y/n) ' choice
    case "$choice" in
      n|N) return;;
      y|Y) break;;
      *) break;;
    esac
done

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
sudo apt install git -y
sudo apt update

# install pyenv
#if ! type "pyenv" > /dev/null; then
#	curl https://pyenv.run | bash
#	export PATH="${HOME}/.pyenv/bin:$PATH"
#	eval "$(pyenv init -)"
#	eval "$(pyenv virtualenv-init -)"
#fi

# https://pycom.io/wp-content/uploads/2020/04/Lesson-2-Setting-up-Pymakr-LoPy4.pdf
# install the python version we want
sudo apt install python3 -y
sudo apt install python3-dev -y
sudo apt install python3-pip -y

version=$(python3 -V)
expected_version="Python 3.9.2"
if [[ $version != *"$expected_version"* ]]; then
	echo "${YELLOW}WARNING: default python3 is not 3.9.2, we need to rebuild it from the source${NC}"
    curl https://pyenv.run | bash
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
	exec $SHELL
	pyenv install 3.9.2
	pyenv global 3.9.2
fi

#sudo apt install virtualenv
#virtualenv 
#sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
#pyenv install 3.9.2
#pyenv global 3.9.2
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
#if ! type "pip3.9" > /dev/null; then
#	wget -P "/usr/local/src/hfs" "https://bootstrap.pypa.io/get-pip.py"
#	sudo python3.9 "/usr/local/src/hfs/get-pip.py"
#	pip install --upgrade setuptools
#	rm -rvf "/usr/local/src/hfs/get-pip.py"
#	#export PATH=/usr/lib/postgresql/14/bin/:$PATH
#	# pip install -r packageName/requrirements.txt
#fi

# Move the required files to public
(cd /usr/local/src/hfs; mv -v *.html "/usr/local/src/hfs/public/")
(cd /usr/local/src/hfs; mv -v *.css "/usr/local/src/hfs/public/")

# make the log file
touch "/usr/local/src/hfs/public/public.log"

# install node
if ! type "node" > /dev/null; then
	echo "${BLUE}INFO: installing Node.js${NC}"

	echo "Installing Node.js v16 from the unoffical arm6l release following this https://gist.github.com/davps/6c6e0ba59d023a9e3963cea4ad0fb516 guide"
	wget -P "/usr/local" https://unofficial-builds.nodejs.org/download/release/v16.9.1/node-v16.9.1-linux-armv6l.tar.gz
	tar -xvzf "/usr/local/node-v16.9.1-linux-armv6l.tar.gz" -C "/usr/local"
	rm -rvf "/usr/local/node-v16.9.1-linux-armv6l.tar.gz"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/bin" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/lib" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/include" "/usr/"
	cp -Rv "/usr/local/node-v16.9.1-linux-armv6l/share" "/usr/"
	rm -rvf "/usr/local/node-v16.9.1-linux-armv6l"
fi

echo "${BLUE}INFO: reinstalling project dependencies${NC}"

# install the required node packages
npm --prefix "/usr/local/src/hfs" install "/usr/local/src/hfs"

# install all requirements for the Bluetooth connectivity
pip3 install bleak==0.14.* --force-reinstall -vvv

# install all requirements for local webserver
# NOTE: compatible numpy versions can be found here https://github.com/matplotlib/matplotlib/blob/ac3d0caf0007389579a5fa2576d95657b03d3f02/doc/devel/min_dep_policy.rst#id1
pip3 install matplotlib==3.6.* --force-reinstall -vvv
#pip3 uninstall numpy -y
apt install python3-numpy -y
sudo apt install libopenjp2-7
python -c "import matplotlib"

# install psql
if ! type "psql" > /dev/null; then
	# requirements for the database management
	wget --quiet -O - "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | sudo apt-key add -
	sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
	sudo apt update
	sudo apt install postgresql-13 -y
	sudo sed -i 's/local   all             postgres                                peer/local   all             postgres                                trust/' '/etc/postgresql/13/main/pg_hba.conf'
	sudo sed -i 's/local   all             all                                     peer/local   all             all                                     trust/' '/etc/postgresql/13/main/pg_hba.conf'
	sudo passwd -d postgres
	sudo systemctl restart postgresql
	sudo systemctl enable postgresql
	sudo psql -U postgres -c "ALTER USER postgres PASSWORD 'admin';"
	su - postgres -c 'psql -c "CREATE TABLE IF NOT EXISTS data (id int, timestamp timestamp, chlf_raw int, chlf_normal real, f_factor real, distance real);"'
fi

# make the Bluetooth application
#echo "[Unit]\nDescription=The Bluetooth service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/python3 /usr/local/src/hfs/bt-central.py\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs-bluetooth.service"

# make the application
echo "[Unit]\nDescription=The local site service for HFS sensor\n\n[Service]\nExecStart=/usr/bin/node /usr/local/src/hfs/server.js\n\n[Install]\nWantedBy=multi-user.target" > "/lib/systemd/system/hfs.service"

# cleanup
sudo apt autoremove -y

# reset the number of retries
echo 'Acquire::Retries "3";' > "/etc/apt/apt.conf.d/80-retries"

# verify installation
python3 -V
pip3 -V
node -v
output=$(node -v)
if [ "$output" != "v16.9.1" ]; then
    echo "${RED}ERROR: build failed, node ${output} is installed instead of node v16.9.1${NC}"
	return 1
fi
npm -v
sudo systemctl status postgresql
su - postgres -c 'psql -c "TABLE data"'

sudo systemctl start hfs.service

# add the 'update' command
u_cmd = 'alias update-hfs="wget -O hfs.zip https://github.com/LESA-RPI/hfs.main/archive/refs/heads/server-ui.zip && sudo unzip -o -j hfs.zip hfs.*/sensor/server/* -d /usr/local/src/hfs/ && rm hfs.zip && (cd /usr/local/src/hfs && sudo mkdir -p public && sudo mv -v *.html public/ && sudo mv -v *.css public/ && sudo touch public/public.log && sudo npm install)"'
sudo sh -c "echo ${u_cmd} >> /etc/bash.bashrc"
source /etc/bash.bashrc

echo "${BLUE}install completed${NC}"
