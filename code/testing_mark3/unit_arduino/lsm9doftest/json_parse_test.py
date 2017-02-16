from arduinoInterface import *
import json
from math import sqrt, atan, pi
from time import sleep

a = arduinoInterface()
a.close()
m = a.findAllPorts()
m = m[len(m)-1]
print 'Opening ', m
a.open(port=m[0],baud=m[1])

def normalize(raw):
    norm = [float(i)/sum(raw) for i in raw]
    return norm

def angle(x,y):
    #Hopper Orientation: -X faces forwards, +Y faces Right
    a =  y
    b =  x
    theta = atan(a/b)
    theta = theta * 180.0 / pi
    #if (a>=0) and (b>=0):
    #    pass
    #if (a<0) and (b>=0):
    #    theta += 90
    #if (a>=0) and (b>=0):
    #    theta += 180
    #if (a>=0) and (b>=0):
    #    theta += 360
    return theta

if(1):
    while(1):
        sleep(0.1)
        s = a.read()
        print s
        try:
            pass
            d = json.loads(s)
            e = {}
            for k in d.keys():
                e[k] = normalize(d[k])
            north = angle(e['mag'][0], e['mag'][1])
            print 'RAW ', d, ',  ', 'Normal ', e, 'Theta N ', north
        except:
            pass
            #print 'ERROR: ', s
else:
    pass
a.close()
