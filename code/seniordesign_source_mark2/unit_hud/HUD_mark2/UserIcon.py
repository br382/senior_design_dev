# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:58:10 2016

@author: rick
"""
#from PIL import Image, ImageTk, ImageDraw
from Camera import *
from Constants import *
from Point2D import *
from Storage import *
from math import cos, sin

class UserIcon():
    
    def __init__(self, user_tag, mobile, elevation_change, pixel_coords, heading, **kwargs):
        self.user_tag = user_tag
        self.mobile = mobile
        self.elevation_change = elevation_change
        self.fill_color = LIME_GREEN
        self.outline_color = LIME_GREEN
        self.pixel_coords = pixel_coords
        self.heading = heading
        
    def drawUserIcon(self, rotation, image, static):
        # x = n*cos(theta)
        # y = n*sin(theta)
        print 'Trying to draw user...'
        x = self.pixel_coords.getX()
        y = HUD_HEIGHT - self.pixel_coords.getY()
        
        # Rotate according to icon heading
        user_heading = rotation
        if (static == 1):
            user_heading = 0
        #polygon_coords = self.rotateIcon(Point2D(x,y), polygon_coords)
        
        # Determine coords of polygon
        polygon_coords = self.getUserIconShapeCoords(x, y, user_heading)
        
        # Draw the icon
        if not self.mobile:
            image.polygon([polygon_coords[0], polygon_coords[1], polygon_coords[2]], fill=self.fill_color, outline=self.outline_color)
        else:
            image.polygon([polygon_coords[0], polygon_coords[1], polygon_coords[2], polygon_coords[3]], fill=self.fill_color, outline=self.outline_color)
        
    def getUserIconShapeCoords(self, x, y, user_heading):
        # STILL NEED TO ACCOUNT FOR ROTATION OF BOTH CAMERA AND BEARING OF THIS USER
        DISTANCE_FROM_CENTER_POINT = 15 #5
        DISTANCE_FROM_CENTER_SIDE = 9 #3
        if not self.mobile:
            #With rotation
            polygon_coords1 = (int(x + DISTANCE_FROM_CENTER_POINT * math.cos(math.radians(90+self.heading + user_heading))), int(y - DISTANCE_FROM_CENTER_POINT * math.sin(math.radians(90+self.heading + user_heading))))
            polygon_coords2 = (int(x + DISTANCE_FROM_CENTER_SIDE * math.cos(math.radians(225+self.heading + user_heading))), int(y - DISTANCE_FROM_CENTER_SIDE * math.sin(math.radians(225+self.heading + user_heading))))
            polygon_coords3 = (int(x + DISTANCE_FROM_CENTER_SIDE * math.cos(math.radians(315+self.heading + user_heading))), int(y - DISTANCE_FROM_CENTER_SIDE * math.sin(math.radians(315+self.heading + user_heading))))
            
            
            #Without rotation
#            polygon_coords1 = (int(x + DISTANCE_FROM_CENTER_POINT * math.cos(math.radians(90))), int(y - DISTANCE_FROM_CENTER_POINT * math.sin(math.radians(90))))
#            polygon_coords2 = (int(x + DISTANCE_FROM_CENTER_SIDE * math.cos(math.radians(225))), int(y - DISTANCE_FROM_CENTER_SIDE * math.sin(math.radians(225))))
#            polygon_coords3 = (int(x + DISTANCE_FROM_CENTER_SIDE * math.cos(math.radians(315))), int(y - DISTANCE_FROM_CENTER_SIDE * math.sin(math.radians(315))))
            
            polygon_coords = [polygon_coords1, polygon_coords2, polygon_coords3]
            #print polygon_coords
            return polygon_coords
        else:
            # TEMP UNTIL 'mobile' IS IMPLEMENTED
            polygon_coords1, polygon_coords2, polygon_coords3, polygon_coords4 = (0,0), (0,0), (0, 0), (0, 0)
            polygon_coords = [polygon_coords1, polygon_coords2, polygon_coords3, polygon_coords4]
            return polygon_coords
            
    def rotateIcon(self, user_coords, polygon_coords):
        rotated_coords = []
        for coord in polygon_coords:
            rx = cos(self.heading) * (coord[0]-user_coords.getX()) - sin(self.heading) * (coord[1]-user_coords.getY()) + user_coords.getX()
            ry = sin(self.heading) * (coord[0]-user_coords.getX()) + cos(self.heading) * (coord[1]-user_coords.getY()) + user_coords.getY()
            rotated_coords.append((rx, ry))
        return rotated_coords
        
    def setIconUserTag(self, updated_tag):
        self.user_tag = updated_tag
        
#    def setIconMotionState(self, updated_motion_state):
#        self.motion_state = updated_motion_state
#        #if motion_state == "moving":            
        
#    def setIconElevationChange(self, updated_elevation_change):
#        self.elevation_change = updated_elevation_change
        
    def getIconUserCoords(self):
        return self.pixel_coords

    def getIconUserTag(self):
        return self.user_tag

#    def getIconMotionState(self):
#        return self.motion_state

#    def getIconElevationChange(self):
#        return self.elevation_change
        