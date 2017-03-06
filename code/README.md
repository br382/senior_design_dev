# Design Overview  

This project combines Arduino based wireless async A/D,
python data/identity intake, storage server, and display GUI.
Each of which are seprate programs which may be split apart,
or run on the same hardware device.
Only ```unit_intake``` owns an auto-generated identity.
All other processes can serve to any identity.
Although primarily for ```unit_display```,
Kivy can be used to build any of the python based units.
To package the ```unit_display``` for Android, Kivy is used.

# Design Diagram  

```
Unit #:

+------------------------------------------------+
|                                                |
|   Optional Sensors + Arduino Interface         |
|                                                |
|  |------------|                  |----------|  |
|  [unit_arduino] Optional Wireless|   Xbee   |  |
|  |         0  | <==============> | Wireless |  |
|  | Sensors :  |  Serial Bridge   |  Serial  |  |
|  |         n  |                  |----------|  |
|  |------------|                        /\      |
|                                        ||      |
|  |------------------------| USB-Serial //      |
|  |     [unit_intake]      |<===========/       |
|  |                        |                    |
|  |   Conversion-Intake    |    /-              |
|  |                        |<====- GPS Receiver |
|  |   Identity Generation  |    \- (Optional)   |
|  |        (.py)           |                    |
|  |------------------------|<======\            |
|                                   \\           |
|                                   ||           |
|  |------------------------|       ||           |
|  |     [unit_server]      |       ||           |
|  |     Storage Server     |       ||           |
|  |     Networked Node     |       ||           |
|  |         (.py)          |<======++> LAN-WiFi |
|  |------------------------|       ||           |
|                                   ||           |
|                                   ||           |
|  |------------------------|       //           |
|  |      [unit_display]    |<======/            |
|  |   Mobile Display Unit  |                    |
|  |                        |   /-               |
|  |         (.py)          |<===- GPS Receiver  |
|  |------------------------|   \- (Optional)    |
|                                                |
+------------------------------------------------+

```


# Code Sections  

- Optional sensors assigned to node are managed by the Arduino.
- Data Intake is consumed, Unit UID is generated, and positioning is updated if equiped.
- Distributed location and sensors information is stored on a Storage Node.
- Display code requests info, and may update positioning if equiped.


# Distributed Architecture  
- Originally designed as a wearable colaboration system.
- System parts may be split onto multiple CPU/MCU devices for a single Unit.
- Units are not required to all have Storage Servers.
- Units are not required to all have a Display Unit.
- Displays do not have Unit UIDs, and an arbitrary amount of displays may exist.
- Storage Servers do not have Unit UIDs, and an arbitary amount of Storage Servers may exist.
- For every Intake Unit, there exists a UID.
- The archetecture does not limit the number of sensors or attached Arduinos, but Intake code modifications may be required to support it.


