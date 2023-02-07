# Setup
The central device (server) has been tested with a *Raspberry Pi Zero W*.

> ### Connectivity Issues
> For whatever reason, RPIs dislike setting themselves up properly. Before continuing, make sure you can `ping google.com` sucessfully. If something seems off, try the following solutions:
> ##### Improper Hostname
> Make sure your hostname has been properly changed, especially if this is a newly installed PI. Type in `sudo nano /ect/hosts` and make sure that the line starting with `127.0.1.1` has the proper hostname and that `sudo nano /etc/hostname` also shows the proper hostname [(source)](https://raspberrypi.stackexchange.com/questions/92751/temporary-failure-in-name-resolution).
> ##### DNS Resolution
> Sometimes the default DNS servers are just bad. Run the command `echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf.head` to add google.com to the list of nameservers to use [(source)](https://raspberrypi.stackexchange.com/questions/64556/problem-with-dns).

To install or update the HFS library in `/usr/local/src/`, run the following command: 

```
wget -O hfs.zip "https://github.com/LESA-RPI/hfs.main/archive/refs/heads/main.zip" && sudo unzip -o -j hfs.zip 'hfs.*/sensor/server/*' -d /usr/local/src/hfs/ && rm hfs.zip
```

Then to build the server dependencies and begin server setup, run:

```
sudo sh /usr/local/src/hfs/install.sh
```

To start the server, simply reboot the PI and both the webpage and bluetooth capabilities will automatically launch.

Finally, one might want to simply update the code on the server. To do so, run:

```
wget -O hfs.zip "https://github.com/LESA-RPI/hfs.main/archive/refs/heads/server-ui.zip" && sudo unzip -o -j hfs.zip 'hfs.*/sensor/server/*' -d /usr/local/src/hfs/ && rm hfs.zip && sudo mv -v "/usr/local/src/hfs/index.html" "/usr/local/src/hfs/public/index.html" 
```