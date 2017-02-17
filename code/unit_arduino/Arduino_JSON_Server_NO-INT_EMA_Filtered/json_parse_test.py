from arduinoInterface import *
import json
from math import sqrt, acos, atan, pi
from time import sleep

a = arduinoInterface()
a.close()
m = a.findAllPorts()
m = m[len(m)-1]
print 'Opening ', m
a.open(port=m[0],baud=m[1])

def spherical(cartesian):
    #Hopper Axis Alignment: -X is Forward, +Y is Right, +Z is Up (Natural Cartesian to degN Correction method).
    # Source: http://mathworld.wolfram.com/SphericalCoordinates.html
    magnitude     = sqrt( sum([abs(i)*abs(i) for i in cartesian]) )
    azimuth_theta = atan(cartesian[1] / cartesian[0])
    polar_phi     = acos(cartesian[2] / magnitude)
    return [magnitude, azimuth_theta, polar_phi]

uid = 0
if(1):
    while(1):
        uid += 1
        if uid > 2: uid = 1
        t = '{"all_data":' + str(uid) + '}'
        print t
        a.write(t)
        sleep(1)
        s = a.read()
        try:
            d = json.loads(s)
            angle = spherical(d['compass_degN'])
            angle[1] = 180.0 * angle[1] / pi
            angle[2] = 180.0 * angle[2] / pi
            #Positive Angles Only For Compass Style Display:
            if angle[1] < 0: angle[1] += 180
            #if angle[2] < 0: angle[2] += 180
            print 'RAW ', s, ',  ', 'Angular (deg)', angle
        except:
            print 'RAW ', s
else:
    pass
a.close()
