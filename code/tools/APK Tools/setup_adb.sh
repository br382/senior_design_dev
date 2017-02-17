sudo bash -c 'echo SUBSYSTEM=="usb", ATTR{idVendor}=="2523", ATTR{idProduct}=="Recon Snow2", MODE=="0666", GROUP=="plugdev" > /etc/udev/rules.d/51-android.rules'
sudo bash -c 'echo 0x2523 > $HOME/.android/adb_usb.ini'
sudo $HOME/android-sdk-linux/tools/android update adb
sudo $HOME/android-sdk-linux/platform-tools/adb kill-server
sudo $HOME/android-sdk-linux/platform-tools/adb start-server
$HOME/android-sdk-linux/platform-tools/adb devices
alias adb=$HOME/android-sdk-linux/platform-tools/adb
cd '$(HOME)/Dropbox/Senior Design/Paintball HUD/code'
sudo $HOME/android-sdk-linux/platform-tools/adb install HUD_Test_2-0.1-debug.apk
