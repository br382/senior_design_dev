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
        self.zoom = 2 #default is 0
        self.rotation = 0
        self.center = Point2D(0, 0)
        self.width = SCOPE_WIDTH * METERS_PER_PIXEL
        self.height = SCOPE_HEIGHT * METERS_PER_PIXEL
        
    #Set zoom level
    def setZoom(self, val):
        self.zoom = val
        
    #Set rotation
    def setRotation(self, val):
        self.rotation = val

    #Set center lat/long value
    def setCenter(self, val1, val2):
        self.center.setX(val1)
        self.center.setY(val2)

#Set width

#Set height

