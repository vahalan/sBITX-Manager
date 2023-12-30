sBITX Telnet Manager
--------------------------------

sBITX Telnet Manager is a tool that provides additional control for the sBITX HF transceiver. This tool uses the telnet protocol interface to send commands to the sBITX for performing remote control of the tranceiver.



Usage
-----

You just need to download and run ```sBITX_manager.py``` or clone the repository.

Right click on the frequency buttons to edit or remove them.

You must open a telnet session from the menu before sending commands to the sBITX. The sBITX app must be running before using the sBITX manager.

Install on you sBITX using terminal:

bash
====
```
$ git clone https://github.com/drexjj/sBITX-Manager.git

$ cd sBITX-manager

$ ./sBITX_manager.py

```


A file named `button_config.json` will be created on first use and stored in the directory of the script.
