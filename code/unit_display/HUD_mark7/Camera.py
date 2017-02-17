# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:00:21 2016

@author: rick
"""
from Point2D import *
from Constants import *

#Initialize with zoom, rotation, center, width, height
class Camera():
    def __init__(self, **kwargs):
        self.zoom = 1 #default is 1
        self.rotation = 0
        self.center = Point2D(0, 0)
        self.width = SCOPE_WIDTH * METERS_PER_PIXEL
        self.height = SCOPE_HEIGHT * METERS_PER_PIXEL
        self.planet = 'earth' #default is 'earth'
        
    #Set zoom level
    def setZoom(self, val):
        if val == UP and self.zoom == 5:
            self.zoom = 1
        elif val == DOWN and self.zoom == 1:
            self.zoom = 5
        elif val == UP:
            self.zoom = self.zoom + 1
        elif val == DOWN:
            self.zoom = self.zoom - 1
        else:
            print 'Issue adjusting the zoom level'
        
    #Set rotation
    def setRotation(self, val):
        self.rotation = float(val)

    #Set center lat/long value
    def setCenter(self, val1, val2):
        self.center.setX(float(val1))
        self.center.setY(float(val2))
        
    def setPlanet(self, val):
        self.planet = val

#Set width

#Set height

