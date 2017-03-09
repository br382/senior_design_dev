#Required Kivy/Buildozer Folders
sudo chmod 777 -R $HOME/.android
sudo chmod 777 -R $HOME/.buildozer

#Source .bashrc if first run of all.sh
source $HOME/.bashrc

#Create a Dummpy Kivy Test App
app_name='my_test_app'
my_dir="$(pwd)"
work_dir=$HOME
cd $work_dir
mkdir ./$app_name
cd $app_name
buildozer init
echo print \'Hello World \!\' > main.py
#cp $my_dir/$app_name.py .

#Make Verbose Logging Output:
sed -i "s/log_level = 1/log_level = 2/g" *.spec
#Correct the App Name:
sed -i "s/package.name = myapp/package.name = $app_name/g" *.spec

#manual android build (debug/release):
# buildozer android debug
# buildozer android release
#manual android install:
# adbsudo start-server
# adbsudo install ./bin/*.apk
# (launch installed .apk via android GUI navigation)
#manual log viwing:
# adbsudo logcat

#Watch Android Debugging Console in new Window:
#(can't use adbsudo here... must write it out.)
gnome-terminal -e 'sudo adb logcat' &
#Automatic build/install/run/debuglog:
buildozer android debug deploy run
chmod 777 ./*

#To List Installed Apps:
sudo adb shell pm list packages

#To remotely remove an app:
#echo "Remotely Removing App"
#$app_name='my_test_app'
adbsudo uninstall org.test.$app_name

#Check for built .apk
echo "===================="
echo "Found .APK Packages:"
find . -iname "*.apk"
echo "===================="

#Return to initial location:
cd $my_dir
