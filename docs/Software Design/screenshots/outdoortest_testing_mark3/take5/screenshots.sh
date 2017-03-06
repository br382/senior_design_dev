name=outdoortest

function adbsudo {
sudo adb "$@"
}

function adbimg {
adbsudo shell screencap /sdcard/$1
adbsudo pull /sdcard/$1
adbsudo shell rm /sdcard/$1
}


i=0
while true; do
  adbimg $name_$i.png
  echo $i
  i=$[$i + 1]
  sleep 1
done
  
