# senior_design_dev  
Using wearable sensors and display devices, communicate through distributed communication servers.
This project was designed to allow relitive location and sensors sharing in the test environment of recreational paintball.
Sensors, hardware devices, and number of units are scalable with the architecture used in this repository.

## Use on Linux Mint/Ubuntu  

### Get Source Files  
- ```sudo apt-get install git```  
- ```git clone https://github.com/br382/senior_design_dev.git```  

### Install Android .APK Build Environment  
- Installs .APK build environment.
- Verifies by building an example ```main.py``` into an ```.apk```.
- ```cd ./senior_design_dev/code/setup/```  
- ```bash all.sh``` 

### Create ```unit_*```  
- Review usage ```./senior_design_dev/code/README.md```
- Follow instructions for each ```./senior_design_dev/code/unit_*/README.md```
- Todo: ```unit_arduino, unit_display``` build/install instructions.

### Load Programs Onto Devices  
- Copy Python, .APK, and Arduino programs to their target hardware devices.
- See hardware/software combined usage ```./senior_design_dev/code/README.md```
- Configure WiFi or other wireless connections between devices.
- Todo: instructions to add Python programs to Raspberry PI/init.d startup.

### Power On Systems  
- Power on all devices.
- Open GUI.
- Verify all systems auto-connect to each other.

## Code  
- This directory contains the raw source dump from the project.
- Todo: cleanup organization of source.

## Docs  
- Design ideology documentation.
- Presentation documentation.
- Demonstration video: [Drexel Homepage](https://www.cs.drexel.edu/~br382/projects.html)
- Todo: cleanup organization of docs.

## Hardware Requirements
- Platform with USB and local LAN/WiFi networking adapter.
- Platform with Python 2.7.x.
- (Optional) Platform with GPS via Android API.
- (Optional) Arduino microcontroller.
- (Optional) Wireless serial bridge.
- (Optional) USB-Serial adapter for wireless serial bridge.
- (Optional) Arduino connected sensors.

## Software Dependencies
- [Kivy](https://kivy.org/#home) - Cross-platform GUI library which provides mobile compatibility.
- [pySerial](https://github.com/pyserial/pyserial) - Cross-platform library for accessing system serial ports.
- socket - Python 2.7.x built-in library for system socket access.
- threading - Python 2.7.x built-in library for system threading.
- lock - Python 2.7.x built-in library for object lock/free access management.
- json - Python 2.7.x built-in library for JSON object serialization.
- math - Python 2.7.x built-in used for geometric transforms and square roots.
- time - Python 2.7.x built-in used for data polling synchronization.
- datetime - Python 2.7.x built-in used for time localization and timestamping.
- [ArduinoJson](https://github.com/bblanchon/ArduinoJson) - (Optional) Arduino JSON library for high level message packaging.

## Project Sub-Libraries
- [arduinoInterface](https://github.com/br382/arduinoInterface) - Used as a basic serial messaging and timing handler.
- [socketExchange](https://github.com/br382/socketExchange) - Used as a basic socket messaging interface.
