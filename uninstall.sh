#!/bin/sh

echo OMX Simple Interface installer

sudo rm -rf /usr/share/omxsi/
echo Removed directory and files

sudo rm -f /usr/share/applications/osi.desktop
sudo rm -f /usr/share/raspi-ui-overrides/applications/osi.desktop
echo Removed desktop entries

echo Uninstall completed successfully