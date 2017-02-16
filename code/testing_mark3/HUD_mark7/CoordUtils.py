# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:00:04 2016

@author: rick
"""
from Point2D import *
from Camera import *
import math
from Constants import *

EQUATORIAL_RADIUS = 6378137 #meters
MEAN_RADIUS_OF_EARTH = 6371000 #meters
FEET_TO_METERS = 0.305
METERS_TO_FEET = 1 / FEET_TO_METERS

def geodeticToPixel(geoPoint, camera):
    ###TO DO:
    #  Handle planet discrepancy
    #  Handle valid lat/lon check
    
#    worldPoint = geodeticToWorldDDDMMSS(geoPoint) #Use if coords are in DDDMMSS format
#    centerPoint = geodeticToWorldDDDMMSS(camera.center) #Use if coords are in DDDMMSS format
    worldPoint = geodeticToWorldDecDeg(geoPoint) #Use if coords are in dec deg format
    centerPoint = geodeticToWorldDecDeg(camera.center) #Use if coords are in dec deg format
#    print 'Center Point (Lat/Lon) = ' + str(camera.center)
#    print 'Center Point (Dec Deg) = ' + str(centerPoint)
#    print 'User Point (Lat/Lon) = ' + str(geoPoint)
#    print 'User Point (Dec Deg) = ' + str(worldPoint)
    distance = getDistanceHaversine(centerPoint, worldPoint)
    #distance = getDistanceLawOfCosines(centerPoint, worldPoint)
    bearing = getBearing(centerPoint, worldPoint)
    finalPoint = worldToPixel(distance, bearing, camera)
    return finalPoint

def ConvertDDDMMSStoDecimalDegrees(dddmmss):
    direction = dddmmss[0]
    ddd = int(dddmmss[1:4])
    mm = int(dddmmss[4:6])
    ss = float(dddmmss[7:])
    dd = ddd + float((mm + float(ss/60))/60)
    if(direction == 'S' or direction == 'W'):
        dd = -dd
    return dd
    
# Convert geodetic coords to world coords
# Return computed world coord as x,y value
def geodeticToWorldDDDMMSS(pointSrc):
    temp1 = ConvertDDDMMSStoDecimalDegrees(pointSrc.getX())
    temp2 = ConvertDDDMMSStoDecimalDegrees(pointSrc.getY())
    pointDest = Point2D(temp1, temp2)
    #print pointDest
    #Latitude = Y-direction, Longitude = X-direction
    world = Point2D(pointDest.getY(), pointDest.getX())
    return world
    
# Convert geodetic coords to world coords
# Return computed world coord as x,y value
def geodeticToWorldDecDeg(pointSrc):
    pointDest = Point2D(pointSrc.getX(), pointSrc.getY())
    #Latitude = Y-direction, Longitude = X-direction
    world = Point2D(pointDest.getY(), pointDest.getX())
    return world
    
def worldToPixel(distance, bearing, camera):
    pixelDistance = distance / METERS_PER_PIXEL
    compassAngle = bearing
    rotationVal = camera.rotation
#    zoomVal = camera.zoom #Original
    #TEST
    if camera.zoom == 5:
        zoomVal = (((HUD_HEIGHT/2.0)-(HUD_HEIGHT/3.0)) / (10.0/METERS_PER_PIXEL)) #30m range
    elif camera.zoom == 4:
        zoomVal = (((HUD_HEIGHT/2.0)-(HUD_HEIGHT/3.0)) / (25.0/METERS_PER_PIXEL)) #75m range
    elif camera.zoom == 3:
        zoomVal = (((HUD_HEIGHT/2.0)-(HUD_HEIGHT/3.0)) / (50.0/METERS_PER_PIXEL)) #150m range
    elif camera.zoom == 2:
        zoomVal = (((HUD_HEIGHT/2.0)-(HUD_HEIGHT/3.0)) / (75.0/METERS_PER_PIXEL)) #225m range
    else:
        zoomVal = 1.0 #300m range
    #TEST
    theta = 0
    
    # Adjust for rotation of camera (wearer)
    compassAngle -= rotationVal
    compassAngle += 360
    compassAngle = compassAngle % 360
    
    # Must reconcile between Cartesian rotation from the x-axis (CCW from x-axis) and compass rotation (CW from y-axis)
    if compassAngle >= 0 and compassAngle <= 90:
        theta = 90 - compassAngle
    else:
        theta = 360 - (compassAngle - 90)
    
    # Must adjust (0,0) to be at center of image instead of top left
    # DOUBlE CHECK THIS MATH
    x = int(HUD_CENTER_X + (zoomVal * (pixelDistance * math.cos(math.radians(theta))))) #ORIGINAL Increase in zoomVal -> increase in pixelDistance
    y = int(HUD_CENTER_Y + (zoomVal * (pixelDistance * math.sin(math.radians(theta))))) #ORIGINAL Increase in zoomVal -> increase in pixelDistance
#    x = int(HUD_CENTER_X + ((pixelDistance * math.cos(math.radians(theta)))/zoomVal)) #Increase in zoomVal -> decrease in pixelDistance
#    y = int(HUD_CENTER_Y + ((pixelDistance * math.sin(math.radians(theta)))/zoomVal)) #Increase in zoomVal -> decrease in pixelDistance
    pixel = Point2D(x,y)
    
    #Clip to confines of scope
    
    # --USE FOR COHEN-SUTHERLAND CLIP
#    pixel = clipToScopeBorderCS(pixel)
    
    # --USE FOR UNIT CIRCLE CLIP
    # If the pixel position is outside of the largest scope circle, place point on that circle at correct angle
    if ((zoomVal * pixelDistance) > HUD_HEIGHT/2): #ORIGINAL
#    if ((pixelDistance / zoomVal) > HUD_HEIGHT/2):
        x = int(HUD_CENTER_X + ((HUD_HEIGHT/2) * math.cos(math.radians(theta))))
        y = int(HUD_CENTER_Y + ((HUD_HEIGHT/2) * math.sin(math.radians(theta))))
        pixel = Point2D(x,y)
    
    return pixel
    
# Determine distance between two world coordinates using Haversine formula
# Return distance in meters
def getDistanceHaversine(startPoint, endPoint):
    #LATITUDE = Y, LONGITUDE = X
    lat1 = math.radians(startPoint.getY())
    lat2 = math.radians(endPoint.getY())
    delta_lat = lat2 - lat1
    delta_lon = math.radians(endPoint.getX() - startPoint.getX())
    
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2) * math.sin(delta_lon/2)
        
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = MEAN_RADIUS_OF_EARTH * b
#    print 'Distance = ' + str(distance)
    return distance

# Determine distance between two world coordinates using distance law of cosines
# Return distance in meters
def getDistanceLawOfCosines(startPoint, endPoint):
    #LATITUDE = Y, LONGITUDE = X
    lat1 = math.radians(startPoint.getY())
    lat2 = math.radians(endPoint.getY())
    delta_lon = math.radians(endPoint.getX() - startPoint.getX())
    a = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(delta_lon))
    distance = MEAN_RADIUS_OF_EARTH * a
#    print 'Distance + ' + distance
    return distance
    
#This is for beginning heading only since we are only worried about distances around 300ft
#The farther the distance, the more the final heading differs from the beginning heading (travelling on an arc)
def getBearing(startPoint, endPoint):
    #LATITUDE = Y, LONGITUDE = X
    lat1 = math.radians(startPoint.getY())
    lat2 = math.radians(endPoint.getY())
    delta_lon = math.radians(endPoint.getX() - startPoint.getX())
    y = math.sin(delta_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    bearing = (math.degrees(math.atan2(y,x)) + 360) % 360 #Correction for negative bearings
    print 'Bearing = ' + str(bearing)
    return bearing
    
# This is to clip a given pixel location if it is outside the area of the scope.
# Cohen-Sutherland-esque methodology    
def clipToScopeBorderCS(pixel):
    global INSIDE
    global LEFT
    global RIGHT
    global BOTTOM
    global TOP
    INSIDE = 0
    LEFT =   1
    RIGHT =  2
    BOTTOM = 4
    TOP =    8
    
    def computeOutCode(x, y):
        code = INSIDE
        
        if (x < MIN_SCOPE_X):
            code = code |  LEFT
        elif (x > MAX_SCOPE_X):
            code = code | RIGHT
        if (y < MIN_SCOPE_Y):
            code = code | BOTTOM
        elif (y > MAX_SCOPE_Y):
            code = code | TOP
        
        return code
    
    x0 = HUD_CENTER_X
    y0 = HUD_CENTER_Y    
    x1 = pixel.getX()
    y1 = pixel.getY()
    x = 0
    y = 0
    
    code = computeOutCode(x1, y1)
    while (code != INSIDE):
        if (code & TOP):
            x = x0 + (x1 - x0) * (MAX_SCOPE_Y - y0) / (y1 - y0)
            y = MAX_SCOPE_Y
        elif (code & BOTTOM):
            x = x0 + (x1 - x0) * (MIN_SCOPE_Y - y0) / (y1 - y0)
            y = MIN_SCOPE_Y
        elif (code & RIGHT):
            y = y0 + (y1 - y0) * (MAX_SCOPE_X - x0) / (x1 - x0)
            x = MAX_SCOPE_X
        elif (code & LEFT):
            y = y0 + (y1 - y0) * (MIN_SCOPE_X - x0) / (x1 - x0)
            x = MIN_SCOPE_X
            
        x1 = x
        y1 = y
        code = computeOutCode(x1,y1)            
    
    pixel = Point2D(x1, y1)
    return pixel
   
#TEST MAIN   
def main():
    this_camera = Camera()
    this_camera.setZoom(1)
    this_camera.setRotation(338)
    this_camera.setCenter('N03742.179', 'E13555.237')
    test_point = Point2D('N03742.183', 'E13555.235')
    pixel_point = geodeticToPixel(test_point, this_camera)
    print pixel_point
    
#    test_point1 = Point2D('N03742.179', 'E13555.237')
#    test_point2 = Point2D('N03742.178', 'E13555.236')
#    updated_point1 = geodeticToWorld(test_point1)
#    updated_point2 = geodeticToWorld(test_point2)
#    print getDistanceHaversine(updated_point1, updated_point2)
#    print getDistanceLawOfCosines(updated_point1, updated_point2)
#    print getBearing(updated_point1, updated_point2)
    
    
if __name__ == "__main__":
    main()