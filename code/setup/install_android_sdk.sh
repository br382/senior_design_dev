#!/bin/bash
cd $HOME
# https://gist.github.com/wenzhixin/43cf3ce909c24948c6e7
#install android sdk
sudo apt-get install openjdk-7-jdk -y
if [[ -a $(ls *.tgz) ]]
  then
  echo 'Tar already downloaded'
else
  echo 'Downloading Tar'
  wget http://dl.google.com/android/android-sdk_r24.2-linux.tgz
  tar -xvf android-sdk_r24.2-linux.tgz
fi

function android {
  $HOME/android-sdk-linux/tools/android "$@"
}
#will do later:
#android update sdk --no-ui
# adb
sudo apt-get install libc6:i386 libstdc++6:i386
# aapt
sudo apt-get install zlib1g:i386

#https://raw.githubusercontent.com/letientai299/scripts/master/download_all_android_sdk.sh
#configure sdk
function install_sdk {
  android update sdk -u -s -a -t "$1"
}

function fetch_non_obsoled_package_indices {
  # Fetch the sdk list using non-https connections
  android list sdk -u -s -a |\
    # Filter obsoleted packages
    sed '/\(Obsolete\)/d' |\
    # Filter to take only the index number of package
    sed 's/^[ ]*\([0-9]*\).*/\1/' |\
    # Remove the empty lines
    sed -n 's/^[^ $]/\0/p'
}

for package_index in  $(fetch_non_obsoled_package_indices)
do
  echo "====================================================================="
  echo "Start to install package:  ${package_index}"
  echo "====================================================================="
  # Auto accept license
  echo -e "y" | install_sdk "${package_index}"
  echo
  echo
done
