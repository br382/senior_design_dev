# senior_design_dev

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
