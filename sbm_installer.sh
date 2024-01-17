#!/bin/bash

# Clone the repository
git clone https://github.com/drexjj/sBITX-Manager.git

# Set the working directory
working_directory="/home/pi/sBITX-Manager"

# Change directory to sBITX-Manager
cd "$working_directory"

# Give execute permissions
chmod +x ./sBITX_manager.py ./sBITX_editor.py

# Create a desktop shortcut for sBITX_manager
echo -e "[Desktop Entry]\nName=sBITX Manager\nExec=sh -c 'cd $working_directory && ./sBITX_manager.py'\nType=Application\n" | sudo tee /usr/share/applications/sBITX_manager.desktop > /dev/null

# Create a desktop shortcut for sBITX_editor
echo -e "[Desktop Entry]\nName=sBITX Editor\nExec=sh -c 'cd $working_directory && ./sBITX_editor.py'\nType=Application\n" | sudo tee /usr/share/applications/sBITX_editor.desktop > /dev/null

# Update the menu
sudo update-desktop-database

echo "sBITX-Manager setup completed successfully! The applications have been added to the Applications Menu"
