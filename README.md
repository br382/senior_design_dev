# senior_design_dev

## Use on Linux Mint/Ubuntu  

### Get Source Files  

- ```sudo apt-get install git```  
- ```git clone https://github.com/br382/senior_design_dev.git```  

### Install/Compile Android .APK GUI  

- ```cd ./senior_design_dev/code/setup/```  
- ```bash all.sh```  

### Create ```unit_*```  
- Review usage ```./senior_design_dev/code/README.md```
- Follow Instructions for each ```./senior_design_dev/code/unit_*/README.md```

### Load Programs Onto Devices  
- Copy Python, .APK, and Arduino programs to their target hardware devices.
- See hardware/software combined usage ```./senior_design_dev/code/README.md```
- Todo, instructions to add Python programs to Raspberry PI/init.d startup.
- Configure WiFi or other wireless connections between devices.

### Power On Systems  
- Power on all devices.
- Open GUI.
- Verify all systems auto-connect to each other.

## code  
- This directory contains the raw source dump from the project.
- Still in its un-curated form.

## docs  
- Design ideology documentation.
- Presentation documentation.
- Demonstration video: [Drexel Homepage](https://www.cs.drexel.edu/~br382/projects.html)

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
