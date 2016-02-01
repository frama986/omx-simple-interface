#!/bin/sh

if [ $# -gt 0 ]; then
   MYHOME=$1
else
   MYHOME="/usr/share/osi"
fi
echo Installation directory: $MYHOME

mkdir $MYHOME
cp -r * $MYHOME
chmod -R 755 $MYHOME

cp osi.desktop /usr/share/applications
cp osi.desktop /usr/share/raspi-ui-overrides/applications