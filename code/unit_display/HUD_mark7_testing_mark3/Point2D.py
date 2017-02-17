# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:58:33 2016

@author: rick
"""

class Point2D:
    def __init__(self, x_init, y_init):
        self.x = float(x_init)
        self.y = float(y_init)

    def shift(self, x, y):
        self.x += x
        self.y += y

    def getX(self):
        return self.x

    def getY(self):
        return self.y
        
    def setX(self, val):
        self.x = float(val)
        
    def setY(self, val):
        self.y = float(val)

    #Print method
    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])