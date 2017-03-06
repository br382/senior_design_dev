#Configuring ADB on Vanilla Mint 17.2 x64
echo "This Script Sets Up the adb environment to 'SEE' the Recon Instruments Snow2 HUD"
#Add ADB entry into the devices file:
sudo bash -c 'echo SUBSYSTEM=="usb", ATTR{idVendor}=="2523", ATTR{idProduct}=="Recon Snow2", MODE=="0666", GROUP=="plugdev" >> /etc/udev/rules.d/51-android.rules'
sudo bash -c 'echo 0x2523 >> $HOME/.android/adb_usb.ini'
#Restart services:
sudo adb kill-server
sudo adb start-server
sudo adb devices
echo " ^ ^ Currently Found Devices on ADB ^ ^"
echo =======================================
echo "Adding ADB functions to your .bashrc "
echo ''
echo         >> $HOME/.bashrc
cat ./bashrc >> $HOME/.bashrc
cat ./bashrc
echo ''
echo "  ^ ^ ^  See Cool ADB Commands  ^ ^ ^ ^"
echo =======================================
sudo adb
