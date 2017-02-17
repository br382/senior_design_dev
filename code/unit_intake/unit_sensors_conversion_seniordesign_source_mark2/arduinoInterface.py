#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 08:33:22 2015

@author: Brett
"""
import serial
from   time import sleep

class arduinoInterface():
    def __init__(self, port=None, baud=9600, cycle_delay=0.01):
        #import serial
        #from   time import sleep
        self.ser         = serial.Serial()
        self.ser.port    = port
        self.ser.baud    = baud
        self.cycle_delay = cycle_delay
        self.ser_buf     = ''
        self.read_delay  = 0
        if (port != None) and (baud != None):
            self.close()
            self.open()
        else:
            if self.findPort(baud=baud):
                print 'Automatically found (PORT, BAUD): ' +str((self.ser.port, self.ser.baud))
            else:
                print 'Unable to automatically find (PORT, BAUD) combination automatically.'
    
    def open(self, port=None, baud=None):
        if (port != None) and (baud != None):
            self.ser.port = port
            self.ser.baud = baud
        self.ser.open()
        return None
    
    def close(self, port=None, baud=None):
        if (port != None) and (baud != None):
            self.ser.port = port
            self.ser.baud = baud
        self.ser.close()
        return None
        
    def closeAll(self, baud=None):
        unable = 0
        po = self.ser.port
        ba = self.ser.baud
        if baud != None:
            self.ser.baud = baud
        for p in self.findAllPorts():
            self.ser.port = p
            try:
                self.ser.close()
            except:
                unable += 1
        self.ser.port = po
        self.ser.baud = ba
        return unable

    def clearBuf(self):
        self.ser_buf = ''
        return None
    
    def findPort(self, baud=None): #connect to first found
        if (baud != None):
            self.ser.baud = baud
        pre = ['/dev/ttyACM', '/dev/ttyUSB', 'COM']
        r = [p+str(n) for p in pre for n in range(0,100)]
        for port in r:
            self.close()
            try:
                self.open(port, self.ser.baud)
                self.ser.port = port
                break
            except:
                pass
        if self.ser.port == None:
            self.ser.baud = None
            return False
        return True
    
    def findAllPorts(self, baud=None): #list all found, but don't connect
        connections = []
        if (baud != None):
            self.ser.baud = baud
        #self.ser.port = None
        pre = ['/dev/ttyACM', '/dev/ttyUSB', 'COM']
        r = [p+str(n) for p in pre for n in range(0,100)]
        for port in r:
            self.close()
            try:
                self.open(port, self.ser.baud)
                connections.append([self.ser.port, self.ser.baud])
            except:
                pass
        return connections
        
    def read(self):
        self.read_delay = 0
        self.clearBuf()
        while self.ser.inWaiting()>0:
            self.ser_buf += str(self.ser.read())
            if self.ser.inWaiting()<=0:
                sleep(self.cycle_delay)
                self.read_delay += self.cycle_delay
        return self.ser_buf
    
    def write(self, input_str=''):
        output_str = str(input_str)
        if len(output_str)>0:
            self.ser.write(output_str)
        return None
    
    def writeln(self, input_str=''):
        print str(input_str)
        self.write(str(input_str) + '\n')
        return None

if __name__ == '__main__':
    a = arduinoInterface()
