# Old JavaScript Server Troubleshooting Documentation

The initial JavaScript server created by the HFs server, which was functional on an obsolete Raspberry Pi Zero, was non-functioning when being put to test on a new Raspberry Pi 4. The Raspberry Pi 4 (or a faster server in general) is necessary to perform the data analysis and future functions required for the desired end-goal of the HFS server. 

This is a document detailing the problems faced, steps taken, and solutions found for the initial JavaScript server.

The server is still non-functioning after these steps, and a new system was taken for ESP32 to Raspberry Pi communications, but the issues presented may still be relevant.

1. ### RPI's New Web Restrictions

The new RPI web / network restrictions posed initial problems with setup of a new server. Some devices can ping google.com, while others cannot. After investigation, it is still unknown if there is MAC address whitelisting or other permissions required, or if there are some potential problems with the ArpaE network connected to the RPI main network.

Additionally, it was determined that the Raspberry Pi itself was not the cause of the issue, given that connection to other networks, both standalone and personal hotspots, allowed for unfettered internet access and the ability to ping google.com

Solutions:
- Use a hotspot for testing
- To be safe, install the server on an unfettered network
- Continue to work with RPI to find the root of the issue

2. ### Raspian: New vs Legacy 

The new version of the Raspbian operating system downloadable from the main Raspberry Pi website was incompatible with the JavaScript server created by the team a few years ago. The legacy version is required for operation.

Solutions:
- Use the legacy version of Raspbian for the Raspberry Pi 4

3. ### Server.js Apostrophe Issues

In JavaScript, there are two types of apostrophes. One is on the top left of a standard US keyboard, denoted as: ` and the other to the left of the enter key on a standard US keyboard, denoted as: '

For text output in JavaScript, the first option is necessary for compilation. In the JS file, the second was used, which lead to no ERROR messages.

This was changed locally to begin debugging the server.js file issues, but nothing on the GitHub was officially changed.

Solution:
- Use the correct form of apostrophe for JavaScript

4. ### Port 3000

After analyzing the error messages and using some research, there appears to be a service in the legacy version of Raspbian used on the Raspberry Pi 4 that uses the 3000 network port. 

This port was changed to 8000 to remove the error.

Solution:
- Use port 8000 (or another port) if 3000 is taken by another service

5. ### Sudo

This is more of a reminder than an error, but every action taken should have "sudo" (superuser / administrator permission) used to prevent partial installations, failed installations, and wasted time.

Solution: 
- Use SUDO command for everything

6. ### Python and Dependency Versions

It appears that some of the versions used initially by the team for the Raspberry Pi Zero project have updated and have some issues with the current setup. 

Python v3.9 should be used, which is not the most recent version.

numpy v1.26.1 is the same version for both then and now. 

Solution:
- Ensure versions are the same and / or compatible

7. ### Matplotlib and Numpy

These python dependencies, used as part of the server, were a large issue. 

A variety of changing, inconsistent errors associated with those two packages prevented the server from running, even though the hfsservice was running on the Raspberry Pi. 

Everything Tried:
- Virtual Environments
- Reinstallation of packages
- Reinstallation of Python and packages
- Changing the versions of packages
- Ensuring all packages were updated to latest version
- Attempting to use packages for alternative uses