sBITX Telnet Manager
--------------------------------

sBITX Telnet Manager is a companion app that provides additional control for the sBITX HF transceiver. This tool uses the telnet protocol interface to send commands to the sBITX for performing remote control of the tranceiver.

![Alt text](images/sbitx-manager.JPG)
![Alt text](images/sbitx-manager2.JPG)
![Alt text](images/sbitx-manager3a.JPG)
![Alt text](images/sbitx-manager4.JPG)


Installation
-----

You can either download and run ```sBITX_manager.py``` or clone the repository.

Install on you sBITX using terminal:
```
git clone https://github.com/drexjj/sBITX-Manager.git

cd sBITX-Manager

chmod +x ./sBITX_manager.py

./sBITX_manager.py

```

Windows Install:
```
Ensure Python is installed and configured on your computer

On the GitHub page, Select Code and Download the zip file

Extract the zip file on your computer

Double-click sBITX_manager.py
```

A file named `sbmanager_config.json` will be created on first use and stored in the directory of the script.



Usage
-----

Right click on the frequency buttons to edit or remove them. The format for frequencies is ```xxxx``` where xxxx is the frequency
such as ```14285``` or ```3850```

You must open a telnet session from the menu before sending commands to the sBITX. The sBITX app must be running on your tranceiver before using the sBITX manager.

You can use this app locally on your sBitx or on a remote computer connected to the same network.

A USB eyboard and mouse are required to add or edit frequencies on the sBitx
