# Arduino Systems
- The DIP switch assigns an ID to the Arduino on the serial channel.
- This allows for multiple Arduino Async Sensor devices per wireless serial channel.
- The DIP switch mechanism is also used to bypass a bug in the SPI library for a sensor, in which it locks up the microcontroller when the SPI sensor is not detected.


```
+-----------------------------------------------------+
|              Arduino Wiring Diagram                 |
|                                                     |
|                       \|/                           |
|                        |                            |
|        |-----------------------------|              |
|  +-----| Xbee Wireless Serial Bridge |              |
|  |     |-----------------------------|     LSB      |
|  |                Rx0 || Tx1             --------|  |
|  |                    ||                / D4     |  |
|  |     |-----------------------------|  | D5 DIP |  |
|  +-----| Arduino Pro Mini 16MHz @ 5V |--| D6  SW |  |
|  |     |-----------------------------|  | D7 to  |  |
|  |      |         ||      ||       |    | D8 GND |  |
|  |      A1       SCL,    D2,D3     A0   \ D9     |  |
|  |      |        SDA      ||       |      -------|  |
|  |      |         ||      ||       |       MSB      |
|  |   ---------  ------  -------  ------             |
|  |   R-R 1kOhm   ACC/   HS-SR04   PSI               |
|  |   V-divider   MAG    DIP=0    DIP=1              |
|  |              DIP=0   -------  ------             |
|  |   ---------  ------    |        |                |
|  |      |         |       |        |                |
|  |      |         |       |        |                |
|  |      |         |       |        |                |
|  |    |------------------------------|              |
|  +----|     Rechargable USB Battery  |              |
|       |------------------------------|              |
|                                                     |
+-----------------------------------------------------+

```


## Arduino JSON Server
- Polls attached hardware sensors.
- Provides required realtime sensor smoothing.
- Listens for data request from serial console.
- When no DIP pins are grounded, the ACC+MAG and HS-SR04(ultrasonic distance) are enabled.
- When only DIP pin digital 4 is grounded, the PSI voltage sensor is enabled.


## MAG_ACC_Test
- Testing the ACC+MAG magnetometer sensor and smoothing algorithms.
- Not complete.


## hw_log_testing
- Test runtime of wireless sensors.
- Test sensor input ranges.

## discontinued_hw_tests
- Individual sensors functionality testing.
- Reference for combined Async code.
