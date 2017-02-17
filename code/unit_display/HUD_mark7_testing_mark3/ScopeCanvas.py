# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:19:29 2016

@author: rick
"""
from Camera import Camera
from kivy.graphics import Color, Line, Rectangle, Triangle
from kivy.core.text import Label as CoreLabel

#import math
from Constants import *
from Point2D import *
from UserIcon import UserIcon
from CoordUtils import geodeticToPixel

def main():
    scope_canvas = ScopeCanvas()
    test_users = dummyUsers(users=3)
    scope_canvas.updateDisplay(test_users)

def dummyUsers(users=3):
    from random import randint
    ret = {}
    for k in range(100,100+users):
        ret[k] = {
            "uid"         :k,   #may be str() or int() but must be same as k (key)
            "name"        :"test uid " + str(k),
            "posStruct"   :{
                "lat":str(  39.9566 + float(randint(-10,10))/10000), #in "deg.xxxxx" #north is pos, south is neg
                "long":str(-75.1899 + float(randint(-10,10))/10000), #in "deg.xxxxx" #east is pos, west is neg
                "heading":randint(0,360),                            #in degrees from north as on a compass
                "altitude":randint(-100,100),                        #in distance units above sea level
                "planet":"earth"
            },
            "markerStruct":{
                "paint_level":randint(0,100),      #current units measured of paint
                "tank_pressure":randint(0,3200),   #PSI of tank
#                "tank_pressure":randint(0,100),   #percentage full of tank
                "tank_pressure_full":3200,         #Full PSI of air tank
                "batteries":[4.8, 3.5],                 #list of battery sensors measured as units (volts?/percentage?)
                "batteries_full":[5.1, 5.1]
            }
            #More keys may exist... but these entries above are guaranteed (per user).
        }
    return ret

def round2Str(number, place=2):
    if place>0:
        label = str(float(number))
        try:
            label = label.split('.')
            label[1] = label[1][0:place]
            label = '.'.join(label)
        except:
            return str(int(number))
        return label
    else:
        return str(int(number))

class ScopeCanvas():
    def __init__(self, canvas, **kwargs):
        self.camera = Camera()
        self.static_background = canvas
        self.static_air_label = CoreLabel(text='Air', font_size=15)
        self.air_label = CoreLabel(text='0%', font_size=15)
        self.static_paint_label = CoreLabel(text='Paint', font_size=15)
        self.paint_label = CoreLabel(text='0%', font_size=15)
        self.heading_label = CoreLabel(text='Heading: 0', font_size=15)
        self.zoom_label = CoreLabel(tex='Zoom: 10m', font_size=15)
        self.paintDisplayBackground()
    def paintDisplayBackground(self):
        with self.static_background:
            #Air (left)
            Color(.5, 1, 0, mode='rgb')
            Line(rectangle=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM, GRAPH_WIDTH, GRAPH_MAX_HEIGHT))
            
            #Static Air Label
            self.static_air_label.refresh()
            texture = self.static_air_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(BAR_TEXT_OFFSET-10, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
            
            #Scope (center) 40-pixel separation between circles (radius)
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-(HUD_HEIGHT/3))) #(Center-x, center-y, radius)
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-(HUD_HEIGHT/6)))
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, HUD_HEIGHT/2))
            
            #Center static icon
            center_pos = Point2D(HUD_CENTER_X, HUD_CENTER_Y)
            staticSelfIcon = UserIcon("Self", False, 0, center_pos, 0)
            staticSelfIcon.drawUserIcon(0, self.static_background, False)
            
            #Paint (right)
            Line(rectangle=(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM, GRAPH_WIDTH, GRAPH_MAX_HEIGHT))
            
            #Static Paint Label
            self.static_paint_label.refresh()
            texture = self.static_paint_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(HUD_WIDTH-BAR_TEXT_OFFSET-GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
            
            #Battery icon
            Line(rectangle=(GRAPH_OFFSET_LEFT_RIGHT, HUD_HEIGHT - BATTERY_ICON_OFFSET_TOP_BOTTOM, BATTERY_ICON_MAIN_WIDTH, BATTERY_ICON_MAIN_HEIGHT))
            Line(rectangle=(GRAPH_OFFSET_LEFT_RIGHT + BATTERY_ICON_MAIN_WIDTH, HUD_HEIGHT - BATTERY_ICON_LEAD_OFFSET_TOP_BOTTOM, BATTERY_ICON_LEAD_WIDTH, BATTERY_ICON_LEAD_HEIGHT))
    def _paintZoomLabel(self):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        if (self.camera.zoom == 1):
            text = 'Zoom: 100m'
        elif (self.camera.zoom == 2):
            text = 'Zoom: 75m'
        elif (self.camera.zoom == 3):
            text = 'Zoom: 50m'
        elif (self.camera.zoom == 4):
            text = 'Zoom: 25m'
        elif (self.camera.zoom == 5):
            text = 'Zoom: 10m'
        else:
            print 'Invalid zoom value'
            
        try:
            with self.static_background:                   
                self.zoom_label.text = text
                self.zoom_label.refresh()
                texture = self.zoom_label.texture
                texture_size = list(texture.size)
                Rectangle(pos=(HUD_CENTER_X + HUD_WIDTH/6, HUD_HEIGHT-20), texture=texture, size=texture_size)
        except:
            print 'Issue drawing zoom label'
            
    def _printHeadingLabel(self):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        try:
            with self.static_background:                   
                self.heading_label.text = 'Heading: '  + str(int(self.camera.rotation))
                self.heading_label.refresh()
                texture = self.heading_label.texture
                texture_size = list(texture.size)
                Rectangle(pos=(HUD_WIDTH/8, HUD_HEIGHT-20), texture=texture, size=texture_size)
        except:
            print 'Issue drawing heading label'
    
    def _paintAirPercentage(self, percentage_full):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        percentage_full = float(percentage_full)
        #ASSUMES PERCENTAGE IN TERMS OF 0 - 100
        with self.static_background:
            if (percentage_full <= 25):
                Color(1, 0, 0, mode='rgb')
            elif (percentage_full <= 50):
                Color(1, 1, 0, mode='rgb')
            else:
                Color(0, 1, 0, mode='rgb')
            level = ((100.0 - float(percentage_full))/100.0) * GRAPH_MAX_HEIGHT
            Rectangle(pos=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-level))
    def _paintAirPercentageLabel(self, percentage_full):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        with self.static_background:                   
            self.air_label.text = round2Str(percentage_full,place=2) + '%'
            self.air_label.refresh()
            texture = self.air_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(GRAPH_WIDTH + BAR_TEXT_OFFSET, HUD_HEIGHT/2), texture=texture, size=texture_size)
    def _paintAirPSI(self, psi, psi_full):
        #ASSUMES PSI BETWEEN 0 AND FULL_TANK_PSI (3200)
        with self.static_background:
            if (psi <= (psi_full/3)):
                Color(1, 0, 0, mode='rgb')
            elif (psi <= (psi_full/2)):
                Color(1, 1, 0, mode='rgb')
            else:
                Color(0, 1, 0, mode='rgb')
            try:
                level = ((100.0 - (float(psi)/float(psi_full))*100.0)/100.0) * GRAPH_MAX_HEIGHT
            except:                
                level = GRAPH_MAX_HEIGHT
                print 'Issue with setting PSI level'
            Rectangle(pos=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-level))
    def _paintAirPSILabel(self, psi):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        with self.static_background:                   
            self.air_label.text = round2Str(psi,place=0) + 'psi'
            self.air_label.refresh()
            texture = self.air_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(GRAPH_WIDTH + BAR_TEXT_OFFSET, HUD_HEIGHT/2), texture=texture, size=texture_size)
    def _paintPaint(self, percentage_full):
        percentage_full = float(percentage_full)
        with self.static_background:
            if (percentage_full <= 25):
                Color(1, 0, 0, mode='rgb')
            elif (percentage_full <= 50):
                Color(1, 1, 0, mode='rgb')
            else:
                Color(0, 1, 0, mode='rgb')
            level = ((100.0 - float(percentage_full))/100.0) * GRAPH_MAX_HEIGHT
            Rectangle(pos=(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-level))
    def _paintPaintLabel(self, percentage_full):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        with self.static_background:                   
            self.paint_label.text = round2Str(percentage_full,place=2) + '%'
            self.paint_label.refresh()
            texture = self.paint_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(HUD_WIDTH - GRAPH_WIDTH - BAR_TEXT_OFFSET - 35, HUD_HEIGHT/2), texture=texture, size=texture_size)
    def _paintBatteryMeters(self, batteries_list, batteries_full_list):
        #In batteries_list, select most lowest-charge battery and display to user
        #batteries_list      = [] #voltages/percentages
        #batteries_full_list = [] #voltages/percentages
        got_first_charge = False
        i = 0
        for battery in batteries_list:
            try:
                temp = battery/batteries_full_list[i] #Determine percentage of full charge
                if not got_first_charge:
                    charge_level = temp
                    got_first_charge = True
                else:
                    if temp < charge_level:
                        charge_level = temp
            except:
                print 'Issue determining battery level for item ' + str(batteries_list[i]) + ' in batteries_list.'
            i = i+1
        print 'Charge percentage of least charged battery is: ' + str(int(charge_level*100)) + "%"
                
        #Draw battery meter
        with self.static_background:
            Color(0, 1, 0, mode='rgb')
            Rectangle(pos=(GRAPH_OFFSET_LEFT_RIGHT, HUD_HEIGHT - BATTERY_ICON_OFFSET_TOP_BOTTOM), size=(BATTERY_ICON_MAIN_WIDTH*charge_level, BATTERY_ICON_MAIN_HEIGHT))
            
    def _paintMainUser(self, user_struct, DEBUG=True):
        try:
            lat          = user_struct["posStruct"]["lat"]
            long         = user_struct["posStruct"]["long"]
            heading      = user_struct["posStruct"]["heading"]               #deg_compass_north
	except:
            if DEBUG:
                lat      = 0
                long     = 0
                heading  = 0
                print 'Using dummy position and heading values...'
        air_value        = user_struct["markerStruct"]["tank_pressure"]      #Uncomment for percentage full
        air_full         = user_struct["markerStruct"]["tank_pressure_full"] #Uncomment for PSI
        paint_percentage = user_struct["markerStruct"]["paint_level"]        #assumed in %
        batteries        = user_struct["markerStruct"]["batteries"]          #list of batteries voltages
        batteries_full   = user_struct["markerStruct"]["batteries_full"]
        #self.paintDisplayBackground() #not needed every time, also paints user-icon
        self.camera.setCenter(lat, long) #args may be int(), float(), or str()
        self.camera.setRotation(heading)
        self._printHeadingLabel()
        self._paintZoomLabel()
#        self._paintAirPercentage(air_value) #Uncomment for percentage full
#        self._paintAirPercentageLabel(air_value) #Uncomment for percentage full
        self._paintAirPSI(air_value, air_full) #Uncomment for PSI
        self._paintAirPSILabel(air_value) #Uncomment for PSI
        self._paintPaint(paint_percentage)
        self._paintPaintLabel(paint_percentage)
        self._paintBatteryMeters(batteries, batteries_full)
    def _paintOtherUsers(self, user_struct):
        name             = user_struct["name"]
        lat              = user_struct["posStruct"]["lat"]
        long             = user_struct["posStruct"]["long"]
        heading          = user_struct["posStruct"]["heading"] #deg_compass_north
        user_coord = Point2D(lat, long) #args may be int(), float(), or str()
        pixel_point = geodeticToPixel(user_coord, self.camera)
        userIcon = UserIcon(name, False, 0, pixel_point, heading)
        userIcon.drawUserIcon(self.camera.rotation, self.static_background, 0)
    def updateDisplay(self, data, uid_me='', DEBUG=True):
        #This method assumes the display is cleared before it is called to repopulate it.
        if DEBUG: print 'uid_me: ', uid_me
        found_me = False
        for k in data.keys():
            if k == uid_me:
                try:
                    self._paintMainUser(data[k])
                    found_me = True
                except Exception as e:
                    print 'ERROR Loading Main UID: ', k
                    print '==========='
                    print e
                    print '==========='
                break
        for k in data.keys():
            if not(k == uid_me) and found_me:
                try:
                    self._paintOtherUsers(data[k])
                except Exception as e:
                    print 'ERROR Loading Other UID: ', k
                    print '==========='
                    print e
                    print '==========='
        if DEBUG: print 'Painted Users: ', found_me

if __name__ == "__main__":
    main()
