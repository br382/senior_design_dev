Python Version:
	* Developement based on 2.7.x, but should be compatable with 3.x (not tested).
HUD Packaging:
	* Kivy is the packaging utility used for portable operating systems like Android and IOS.
	* For testing the .apk see `.../Dropbox/Senior Design/Paintball HUD/code/APK_Test/Install ADB for linux.txt`
	   which can be used for debugging a live running .apk program on Android.
	* A hello-world .apk test instructions are at: `.../Dropbox/Senior Design/Paintball HUD/code/APK_Test/README.txt`.
GUI Code Requirements:
	* PIL installer is needed for windows testing environments but is included in n'ix installations of python.
	* Kivy, Tkinter, or something to display the rendered JEPG in a GUI.
Server Code Requirements:
	* No Dependancies.
Sensor Code Requirements:
	* PySerial is used in code interfacing with the Arduino,
	   and is pre-installed on most RaspberryPi OS's,
	   but is needed for windows or other desktop OS's (use `python setup.py install` from .zip contents).
Arduino Code Requirements:
	* ArduinoJson.zip inserted into the Arduino IDE client from: https://github.com/bblanchon/ArduinoJson
