sBITX Manager v2.0
--------------------------------

sBITX Manager is a companion app that provides additional control for the sBITX HF transceiver using the telnet protocol. 

Here is a list of features:
- Provides a user-friendly interface for interacting with the sBITX transceiver
- Frequency memory management allows for adding, editing, and removal of frequencies and settings
- A memory scan function that scans through the list of stored frequencies at a customized interval
- Sends command specifying details such as VFO, Step, Mode, Bandwidth, IF, AGC, Audio, and more
- Decodes messages in FT8 and CW modes
- Text adjustment for better readabilitiy on larger screens
- Configuration is stored in a file, enabling easy transfer between devices and eliminating the need for manual entry of new memories
- Includes a an app to reorder memories in the config file called sBITX editor

![Alt text](images/sbitx-manager1.JPG)
![Alt text](images/sbitx-manager2.JPG)
![Alt text](images/sbitx-manager3.JPG)
![Alt text](images/sbitx-manager4.JPG)
![Alt text](images/sbitx-manager5.JPG)
![Alt text](images/sbitx-manager6.JPG)
![Alt text](images/sbitx-manager7.JPG)


Installation
-----

You can either download and run ```sbm_installer.sh``` or clone the repository and run ```sbm_installer.sh```. See below.

Install on you sBITX or Linux using terminal (Method 1):
```
curl -O https://raw.githubusercontent.com/drexjj/sBITX-Manager/main/sbm_installer.sh

chmod +x ./sbm_installer.sh

./sbm_installer.sh

```

Install on you sBITX or Linux using terminal (Method 2):
```
git clone https://github.com/drexjj/sBITX-Manager.git

cd sBITX-Manager

chmod +x ./sbm_installer.sh

./sbm_installer.sh

```

Windows 10/11 Install:

Download the Windows release from [Windows Releases](https://github.com/drexjj/sBITX-Manager/releases/tag/Windows) and unzip to the file to a folder of your choosing.

OR

Ensure Python version 3 is installed and configured on your computer

On the GitHub page, Select Code and Download the zip file

Extract the zip file on your computer

Double-click sBITX_manager.py


A file named `sbmanager_config.json` will be created on first use and stored in the directory of the script. ``Make a backup of this file before upgrading to newer versions``



Usage
-----

You must open the telnet session from the menu before sending commands to the sBITX. The sBITX app must be running on your tranceiver before using the sBITX manager.
If you run into issues, restart the sBitx app on the transceiver and restart sBitx_Manager.

You can use this app on your sBitx or on a remote computer connected to the same network.

A USB keyboard and mouse are required to add or edit frequencies on the sBitx
