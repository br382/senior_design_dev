"""
@Author Brett, Rick
"""
import json
from arduinoInterface import *
from Database         import *
from constants        import *
from uidGen           import uidGen
from math             import sqrt, acos, atan, pi

def spherical(cartesian):
    #Hopper Axis Alignment: -X is Forward, +Y is Right, +Z is Up (Natural Cartesian to degN Correction method).
    # Source: http://mathworld.wolfram.com/SphericalCoordinates.html
    magnitude     = sqrt( sum([abs(i)*abs(i) for i in cartesian]) )
    azimuth_theta = atan(cartesian[1] / cartesian[0])
    polar_phi     = acos(cartesian[2] / magnitude)
    return [magnitude, azimuth_theta, polar_phi]

class Sensor():
    def __init__(self, port=None, baud=None, xbee_uid_range=2**(9-4+1), DEBUG=False):
        self.DEBUG = DEBUG
        self.xbee_uid_range   = xbee_uid_range #max with current Arduino firmware is 2^6
        self.xbee_uid         = 0
        self.data             = Database()
        self.data.in_json_obj = {}
        self.myUID            = uidGen()
        if (port == None or baud == None):
            self.arduino = arduinoInterface()
        else:
            self.arduino = arduinoInterface(port, baud)
        self.arduino.cycle_delay = 0.05
        self.data.addUser(self.myUID, name=str(self.myUID), safe=False)
        self.response_delay = 0
    def work(self):
        if self.DEBUG: print 'DEBUG ON'
        if self.DEBUG: print 'Scan Range ', externLocalIP()
        if self.DEBUG: print 'Servers ', self.data.servers
        self.response_delay = 0
        #One Iteration of work
        self._requestDataAll()
        self._processPaintLevel()
        self._processPsiLevel()
        self._processBatteryVoltage()
        self._processDistance()
        self._processHeading()
        self.data.users[self.myUID]['last_modify'] = readtimestamp(timestamp())
        temp = self.data.users[self.myUID]['markerStruct']
        temp['uid'] = self.myUID
        self.data.out_json_obj               = {'update_marker': temp}
        self.data.socketExchangeAuto( json.dumps(self.data.out_json_obj) )
    def _requestDataAll(self):
        self.xbee_uid = 1 + (self.xbee_uid % self.xbee_uid_range) # range: [1,max]
        self._requestData( {'all_data':int(self.xbee_uid)} ) #'{"all_data":1}'
    def _requestData(self, data_struct_msg={}):
        request        = data_struct_msg 
        request_output = json.dumps(request)
        try:
            self.arduino.writeln(request_output)  #Send request to Arduino
            data_serial = ''
            tic         = timestamp()
            while len(data_serial)<=0:
                data_serial     = self.arduino.read()  #Recieve data from Arduino
                if timestamp() - tic > 1.0:
                    break
            self.response_delay += timestamp() - tic
            if self.DEBUG: print "Response Delay: " + str(self.response_delay)
            if self.DEBUG: print 'Response STR: ', data_serial
            self.data.in_json_obj = json.loads(data_serial) #Converts str to python data structure
            if self.DEBUG: print 'VALID JSON'
        except:
            try: #if usb-com unplugged after program is started... reconnect.
                self.arduino.close()
                self.arduino.open()
            except:
                pass
            self.data.in_json_obj = {}
            if self.DEBUG: print 'INVALID JSON'
    def _processPaintLevel(self):
        if self._processAccData():
            reading         = self.data.in_json_obj["sonic_us"][0]
            percentage_full = 100.0 - (((reading - HOPPER_FULL_TIME_uS) / (HOPPER_EMPTY_TIME_uS - HOPPER_FULL_TIME_uS)) * 100.0)
            if self.DEBUG: print 'percentage_full: ' + str(percentage_full)
            if (percentage_full > 100):
                percentage_full = 100
            elif (percentage_full < 0):
                percentage_full = 0
            self.data.users[self.myUID]['markerStruct']['paint_level']      = int(percentage_full)
            if self.DEBUG: print 'Percentage Full: ', percentage_full
            self.data.users[self.myUID]['markerStruct']['paint_level_full'] = 100
        else:
            pass
    def _processPsiLevel(self):
        try:
            #Loss of precision occurs, but not of concern here (~10PSI) (due to json output to server).
            psi_level = self.data.in_json_obj["pressure_bits"][0]
            psi_level = (psi_level / 206.0) + 0.034
            psi_level = psi_level * PSI_PER_VOLT + PSI_OFFSET
            if self.DEBUG: print 'psi_level/full ', psi_level,'/',PSI_FULL
        except:
            psi_level = 0
        if psi_level > 0:
            self.data.users[self.myUID]['markerStruct']['tank_pressure']  = psi_level
        self.data.users[self.myUID]['markerStruct']['tank_pressure_full'] = PSI_FULL
    def _processAccData(self):
        try:
            temp = self.data.in_json_obj["acc_g"]
        except:
            temp = []
        acc =  []
        for elm in temp:
            acc.append(elm)
        try:
            use_paint_level_data = (acc[2] > ACC_THRESH_FOR_READ_Z)
        except:
            use_paint_level_data = False
        if self.DEBUG: print 'Use Paint Level? ', use_paint_level_data
        return use_paint_level_data
    def _processBatteryVoltage(self):
        try:
            batt_voltage = self.data.in_json_obj["battery_bits"][0]
            batt_voltage = (batt_voltage / 206.0) + 0.034
            batt_voltage = batt_voltage*2
            print 'Battery Voltage: ', batt_voltage
            #create battery array for each client serial device...
            while (len(self.data.users[self.myUID]['markerStruct']['batteries'])<self.xbee_uid_range):
                self.data.users[self.myUID]['markerStruct']['batteries'].append(None)
            while (len(self.data.users[self.myUID]['markerStruct']['batteries_full'])<self.xbee_uid_range):
                self.data.users[self.myUID]['markerStruct']['batteries_full'].append(None)
            # shift [1,N] indexing to [0,N-1] safely for xbee batteries
            self.data.users[self.myUID]['markerStruct']['batteries'][(self.xbee_uid-1)%self.xbee_uid_range]      = batt_voltage
            self.data.users[self.myUID]['markerStruct']['batteries_full'][(self.xbee_uid-1)%self.xbee_uid_range] = BAT_FULL
            if self.DEBUG: print 'batteries ', self.data.users[self.myUID]['markerStruct']['batteries']
        except:
            pass #batt_voltage = self.data.users[self.myUID]['markerStruct']['batteries']
    #def _processVelocity(self):
    #    try:
    #         velocity = self.data.in_json_obj["velocity_ms"][0]
    #    except:
    #        velocity = 0            
    #    self.data.users[self.myUID]['pointStruct']['velocity'] = velocity
    def _processDistance(self):
        try:
            distance = self.data.in_json_obj["dist_mm"][0]
            self.data.users[self.myUID]['pointStruct']['dist_mm'] = distance
            if self.DEBUG: print 'dist_mm ', distance
        except:
            pass #distance = self.data.users[self.myUID]['pointStruct']['dist_mm']
    def _processHeading(self):
        try:
            mag = self.data.in_json_obj["magnetometer"]
            if self.DEBUG: print 'magnetometer ', mag
            angle = spherical(mag)
            angle[1] = 180.0 * angle[1] / pi
            angle[2] = 180.0 * angle[2] / pi
            #Positive Angles Only For Compass Style Display:
            if angle[1] < 0: angle[1] += 180
            #if angle[2] < 0: angle[2] += 180
            if self.DEBUG: print 'spherical ', angle
            deg = angle[1]
            self.data.users[self.myUID]['markerStruct']['mag_heading'] = deg
            if self.DEBUG: print 'heading ', self.data.users[self.myUID]['markerStruct']['mag_heading']
        except:
            pass


def main():
    from time import sleep
    xbees = 2
    hz = 1*xbees
    period = 1/float(hz)
    
    a = arduinoInterface()
    a.close()
    m = a.findAllPorts()
    if len(m)>0:
        m = m[len(m)-1]
    else:
        print 'Ports Found: ', m
        print 'Exiting...'
        return #ORIGINAL
    print 'Opening ', m
    #sense = Sensor(port='COM1', baud=9600)
    sense = Sensor(port=m[0],baud=m[1], xbee_uid_range=xbees, DEBUG=True) #ORIGINAL
    while(1):
        print timestamp()
        sense.work()
        print "Period:        " + str(period)
        print "Arduino Delay: " + str(sense.response_delay)
        print timestamp()
        print ''
        sleep(max(period - sense.response_delay,0))

if __name__ == '__main__':
    main()
