SETUP AND USE INSTRUCTIONS:

1. Download: https://codeload.github.com/pyserial/pyserial/zip/master
2. Extract Files
3. Locate 'setup.py'
4. Run: 'sudo python setup.py install'
5. Upload '*.ino' to Arduino
6. Connect Sensors to analog input pins.
7. Connect V_REF_PIN to the regulated 5V pin.
8. Run '*.py' python logging script.
9. Disconnect USB cable to automatically stop logging.
10.Open 'data.csv' in any software to analyse data.
11.Repeat usage as nessisary, the logging script only appends to the end of the file.

PROPERTIES:
  .py  code
    * Loops over all available windows 'COMxx' ports,
      opening the first available it finds.
    * Appends, if it exists, to 'data.csv'.
    * CSV Line Format:
      'milliseconds,PIN_A0,PIN_A1,PIN_A2,PIN_A3,PIN_A4,PIN_A5\n'
    * Binary Values Range: [0,1023]
    * Analog Values Range: [0 volts, V_REF_PIN], (normally V_REF_PIN = 5 volts)

  .ino code
    * Usual Sampling Period:
      'Arduino UNO R3'
      at '9600 baud'
      is 30.00 +/- 0.05 milliseconds.
    * Serial Bus Data Formatting:
      'milliseconds\tPIN_A0\tPIN_A1\tPIN_A2\tPIN_A3\tPIN_A4\tPIN_A5\n'
    * Binary Values Range: [0,1023]
    * Analog Values Range: [0 volts, V_REF_PIN], (normally V_REF_PIN = 5 volts)