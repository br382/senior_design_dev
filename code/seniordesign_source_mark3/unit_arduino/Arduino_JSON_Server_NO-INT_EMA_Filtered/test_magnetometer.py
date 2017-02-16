"""
@Author Brett, Rick
"""
import json
from arduinoInterface import *
from math             import sqrt, acos, atan, pi
from time             import sleep

def spherical(cartesian):
    #Hopper Axis Alignment: -X is Forward, +Y is Right, +Z is Up (Natural Cartesian to degN Correction method).
    # Source: http://mathworld.wolfram.com/SphericalCoordinates.html
    magnitude     = sqrt( sum([abs(i)*abs(i) for i in cartesian]) )
    azimuth_theta = atan(cartesian[1] / cartesian[0])
    polar_phi     = acos(cartesian[2] / magnitude)
    return [magnitude, azimuth_theta, polar_phi]

a = arduinoInterface()
l = a.findAllPorts()
a.close()
l = l[len(l)-1]
print 'Opening Port: ', l
a.open(port=l[0],baud=l[1])

while(1):
    a.write('{"all_data":1}')
    sleep(0.05)
    json_str = a.read()
    try:
        json_obj = json.loads(json_str)
        mag_obj  = json_obj["magnetometer"]
        angle = spherical(mag_obj)
        angle[1] = 180.0 * angle[1] / pi
        angle[2] = 180.0 * angle[2] / pi
        #Positive Angles Only For Compass Style Display:
        #if angle[1] < 0: angle[1] += 180
        #if angle[2] < 0: angle[2] += 180
        print 'spherical ', angle
    except:
        pass #print 'ERROR: `' + str(json_str) + '`'
	sleep(0.5)
a.close()