#!/bin/bash

# Set the working directory
working_directory="/home/pi/sBITX-Manager"

# Clone the repository and refresh local copy
if [ -d "$working_directory" ]; then
    cd "$working_directory"    
    git reset --hard
    git pull
else
    git clone https://github.com/drexjj/sBITX-Manager.git "$working_directory"
    if [ $? -ne 0 ]; then
        echo "Error cloning the repository. Exiting."
        exit 1
    fi
fi

# Change directory to sBITX-Manager
cd "$working_directory"

# Give execute permissions
chmod +x ./sBITX_manager.py ./sBITX_editor.py ./sbm_installer.sh ./sbm_uninstaller.sh

# Create a desktop shortcut for sBITX_manager
echo -e "[Desktop Entry]\nName=sBITX Manager\nExec=sh -c 'cd $working_directory && ./sBITX_manager.py'\nType=Application\n" | sudo tee /usr/share/applications/sBITX_manager.desktop > /dev/null

# Create a desktop shortcut for sBITX_editor
echo -e "[Desktop Entry]\nName=sBITX Editor\nExec=sh -c 'cd $working_directory && ./sBITX_editor.py'\nType=Application\n" | sudo tee /usr/share/applications/sBITX_editor.desktop > /dev/null

# Update the menu
sudo update-desktop-database

echo "sBITX-Manager setup completed successfully! The applications have been added to the Applications Menu"
