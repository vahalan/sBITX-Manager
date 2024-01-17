#!/bin/bash

# Remove the sBITX-Manager directory
cd /home/pi
sudo rm -rf /home/pi/sBITX-Manager

# Remove desktop shortcuts
sudo rm /usr/share/applications/sBITX_manager.*
sudo rm /usr/share/applications/sBITX_editor.*

# Update the menu cache
sudo update-desktop-database

echo "sBITX-Manager application and menu shortcuts have been successfully uninstalled."
