#!/bin/sh
# /etc/init.d/senior_design_startup.sh



#Copy these folders to $HOME: {unit_server, unit_sensors_conversion}
#Then run this install script (for auto-startup on system boot before login):
name="$HOME/.senior_design_mark3"
rm -rf $name
mkdir $name
cp -r ./unit_server $name
cp -r ./unit_sensors_conversion $name
run='startup.sh'
echo '#!/bin/sh
### BEGIN INIT INFO
# Provides:  senior_design_startup
# Required-Start: $all
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Starts server and serial comm.
# Description: Starts the unit_server and unit_sensors_conversion for senior design project.
### END INIT INFO
' > $name/$run
echo "
case \"\$1\" in
	start)
		echo \"starting senior design services\"
		sudo python $name/unit_server/main.py &
		sudo python $name/unit_sensors_conversion/main.py &
		echo \$?
                exit 0
		;;
	stop)
		echo \"stopping senior design services\"
		sudo pkill python
		echo \$?
		exit 0
		;;
	*)
		echo \"Usage: /etc/init.d/startup.sh {start|stop}\"
		exit 1
		;;
esac
" >> $name/$run #/dev/null
#echo "sudo python $name/unit_server/main.py &" >> $name/$run
#echo "sudo python $name/unit_sensors_conversion/main.py &" >> $name/$run
echo "exit 0" >> $name/$run
sudo chmod a+x $name/$run
sudo update-rc.d -f $run remove
sudo cp $name/$run /etc/init.d/$run
sudo chmod 755 /etc/init.d/$run
sudo update-rc.d $run defaults
