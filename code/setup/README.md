# Installation of Prerequisites

## Install/Build Python 2.7.x GUI for Android

* ```./all.sh```

OR sepreately:

* ```./install_kivy.sh```
* ```./install_adb.sh```
* ```./config_adb.sh```
* ```./config_kivy.sh```
* ```./create_app.sh```
* Manually test your app, using comments from ```create_app.sh```, and ```bashrc```

## Notes

* Assumed Android Device:
    - Recon Snow2
    - Set to development mode in settings menu
    - Connected via USB during install
    - ```bashrc``` utility functions installed

* ```install_android_sdk.sh```:
    - Installs excessive number of SDKs via looping over non-obsolete packages.
    - Will take excessive SDK installation time.

