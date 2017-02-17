# Design Overview  

```
Unit #:

+------------------------------------------------+
|                                                |
|   Optional Sensors + Arduino Interface         |
|                                                |
|  |-----------|                  |----------|   |
|  | Sensor 0  |  Digital/Analog  |          |   |
|  |    |      | <==============> | Arduino  |   |
|  |    \/     |                  |          |   |
|  |-----------|                  |----------|   |
|                                        /\      |
|                                        ||      |
|  |------------------------|            ||      |
|  |                        |            //      |
|  |   Sensors Data         |<===========/       |
|  |                        |                    |
|  |   Conversion-Intake    |    /-              |
|  |                        |<====- GPS Receiver |
|  |   Identity Generation  |    \- (Optional)   |
|  |                        |                    |
|  |                        |<======\            |
|  |------------------------|       \\           |
|                                   ||           |
|                                   ||           |
|  |------------------------|       ||           |
|  |                        |       ||           |
|  |     Storage Server     |       ||           |
|  |     Networked Node     |       ||           |
|  |                        |<======++> LAN-WiFi |
|  |------------------------|       ||           |
|                                   ||           |
|                                   ||           |
|  |------------------------|       //           |
|  |                        |<======/            |
|  |   Mobile Display Unit  |                    |
|  |                        |   /-               |
|  |                        |<===- GPS Receiver  |
|  |------------------------|   \- (Optional)    |
|                                                |
|                                                |
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


