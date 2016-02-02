# omx-simple-interface
###A simple interface for OMXPlayer written in Python

This is my first Python project and i decided to share it with everyone.
I created this simple interface for OMXPlayer as a case study to learn Python and, obviously, to semplify the selection of videos.

#####Requirement
* This application is written for Python 3.2 ([Python.org](https://www.python.org/))
* OMXPlayer. You can find information about it here [huceke/omxplayer](https://github.com/huceke/omxplayer).
* Assign the write permissions to the project folder: the application has to create the recent videos' file.


#####Install the application
You have to download all files into a desired folder (ex. into a temporary folder of Desktop)
Open the shell and launch the `install.sh` file with root privileges

    sudo ./install.sh
  
This script will copy all needed files into `/usr/share/omxsi` and put the desktop entry into

    /usr/share/applications
    /usr/share/raspi-ui-overrides/applications

#####Run the application
Now you have just to launch `OMX Simple Interface` application by the Menu or, if you prefer, you can select this application for video files and then run the player with a simple double-click on your video.

#####Uninstall the application
Open the shell and launch the `uninstall.sh` file with root privileges

    sudo ./uninstall.sh
