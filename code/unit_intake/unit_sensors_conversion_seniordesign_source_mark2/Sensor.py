"""
@Author Ken Hale, Brett, Rick

pi_to_arduino Sensor Data
:
This revision uses stores information in the basic DataStruct.userStruct()
but adds any temporary data to the base dict() it generates.
When sending to the server, all temp is removed by DataStruct.cleanUserStruct(struct)
"""
import json
from arduinoInterface import *
from DataStruct       import *
from constants        import *
from SendToServer     import *

class Sensor():
    def __init__(self, port=None, baud=None):
        self.json_input           = {}
        if (port == None or baud == None):
            self.arduino = arduinoInterface()
        else:
            self.arduino = arduinoInterface(port, baud)            
        self.user                 = userStruct()
        self.user['uid']          = 0 #set before sending to server
        self.user['name']         = 'Dummy'
        self.user['first_modify'] = readtimestamp(timestamp())
        self.response_delay       = 0
        SOCKETHOST = socket.gethostname() #'localhost'
        SOCKETPORT = 12345
        self.SOCKET     = (SOCKETHOST, SOCKETPORT)
    def work(self):
        self.response_delay = 0
        #One Iteration of work
        self._requestDataAll()
        print json.dumps(self.json_input)
        self._processPaintLevel()
        self._processPsiLevel()
        self._processBatteryVoltage()
        self._processDistance()
        self._processHeading()
        self.user['last_modify'] = readtimestamp(timestamp())
        print json.dumps(self.user, indent=4, sort_keys=True)
        send = {'update_user': self.user}
        socketEchange(json.dumps(send), self.SOCKET)
        
    
    def _requestDataAll(self):
        self._requestData({'all_data':int(True)}) #{'all_data':1}
    
    def _requestData(self, data_struct_msg={}):
        request        = data_struct_msg 
        request_output = json.dumps(request)
        try:
            self.arduino.writeln(request_output)  #Send request to Arduino
            data_serial = ''
            tic = timestamp()
            while len(data_serial)<=0:
                data_serial     = self.arduino.read()  #Recieve data from Arduino
                if timestamp() - tic > 1.0:
                    break
            self.response_delay += timestamp() - tic
            print "Response Delay: " + str(self.response_delay)
            self.json_input = json.loads(data_serial) #Converts str to python data structure
        except:
            self.json_input = {}
            #for testing (dummy data):
            #self.json_input = {"acc_g":[484,489,654],"compass_degN":[546,123,456],"sonic_ms":[6546]}
    
    def _processPaintLevel(self):
        if self._processAccData():
            reading = self.json_input["sonic_us"][0]
            #For now, assume 100ms is full and 400ms is empty (per data current as of 6 FEB)
            #Subtract 'full' from 'reading' to normalize and divide by difference between 'empty' and 'full'; subtract from 100%
            percentage_full = 100.0 - (((reading - HOPPER_FULL_TIME_uS) / (HOPPER_EMPTY_TIME_uS - HOPPER_FULL_TIME_uS)) * 100.0)
            print 'percentage_full: ' + str(percentage_full)
            #Must account for percentages above 100% and below 0% (disregard and overwrite them)
            if (percentage_full > 100):
                percentage_full = 100
            elif (percentage_full < 0):
                percentage_full = 0
            self.user['markerStruct']['paint_level']      = int(percentage_full)
            print 'Percentage Full: ',percentage_full
            self.user['markerStruct']['paint_level_full'] = 100
        else:
            pass
    
    def _processPsiLevel(self):
        #Need code here to read from external ADC
        try:
            #Loss of precision occurs, but not of concern here (~10PSI)
            psi_level = self.json_input["pressure_bits"][0]
            psi_level = (psi_level / 206.0) + 0.034
            psi_level = psi_level * PSI_PER_VOLT + PSI_OFFSET
            
        except:
            psi_level = 0
        
        self.user['markerStruct']['tank_pressure'] = psi_level
        
    def _processAccData(self):
        try:
            temp = self.json_input["acc_g"]
        except:
            temp = []
        acc =  []
        for elm in temp:
            acc.append(elm)
        print acc
        try:
            use_paint_level_data = (acc[2] > ACC_THRESH_FOR_READ_Z)
        except:
            use_paint_level_data = False
        print 'Use Paint Level? ', use_paint_level_data
        return use_paint_level_data
        
    def _processBatteryVoltage(self):
        try:
            batt_voltage = self.json_input["battery_bits"][0]
            batt_voltage = (batt_voltage / 206.0) + 0.034
            batt_voltage = batt_voltage*2
            print 'Battery Voltage: ', batt_voltage
            self.user['markerStruct']['batteries'] = batt_voltage
        except:
            pass #batt_voltage = self.user['markerStruct']['batteries']
            
        
        
#        def _processVelocity(self):
#            try:
#                velocity = self.json_input["velocity_ms"][0]
#            except:
#                velocity = 0
#                
#            self.user['pointStruct']['velocity'] = velocity
        
    def _processDistance(self):
        try:
            distance = self.json_input["dist_mm"][0]
            self.user['pointStruct']['dist_mm'] = distance
        except:
            pass #distance = self.user['pointStruct']['dist_mm']
        
    def _processHeading(self):
        try:
            deg = self.json_input["compass_degN"][0]
            self.user['pointStruct']['deg_N'] = deg
        except:
            pass #deg = self.user['pointStruct']['deg_N']
            
        

def main():
    from time import sleep
    hz = 1
    period = 1/hz
    #sense = Sensor(port='COM1', baud=9600)
    sense = Sensor(port='COM18', baud=9600)
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
