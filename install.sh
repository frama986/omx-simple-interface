#!/bin/sh

echo OMX Simple Interface installer

MYHOME="/usr/share/omxsi"
echo Installation directory: $MYHOME

mkdir $MYHOME
echo Directory created

cp -r * $MYHOME
chmod -R 755 $MYHOME
chmod -R 777 $MYHOME/data
echo Files copied

cp osi.desktop /usr/share/applications
cp osi.desktop /usr/share/raspi-ui-overrides/applications
echo Desktop entries created

echo Intallation terminated successfully