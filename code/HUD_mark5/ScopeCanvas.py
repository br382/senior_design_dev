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

HEADING = 360

def main():
    scope_canvas = ScopeCanvas()
    #static_background = Image.open("HUD_display.jpg")
    #scope_canvas._paintAirPercentage(86,static_background)
    #scope_canvas._paintAirPSI(2500, static_background)
    #scope_canvas._paintPaint(9, static_background)
    user_data = {'My Coords': ['N03742.179', 'E13555.237'], 
                 'My Heading': HEADING, 
                 'Paint': 33, 
                 'Air': 2400, 
                 'Users':{1018: ['N03742.178', 'E13555.236', 210], 
                          2022: ['N03742.181', 'E13555.240', 270],
                          2023: ['N03742.183', 'E13555.235', 103]
                          }
                }
    scope_canvas.updateDisplay(user_data)
    
    #static_background.save("HUD_display_updated.jpg")
    

class ScopeCanvas():
    
    def __init__(self, canvas, **kwargs):
        self.camera = Camera()
        self.static_background = canvas
        self.static_air_label = CoreLabel(text='Air', font_size=15)
        self.air_label = CoreLabel(text='0%', font_size=15)
        self.static_paint_label = CoreLabel(text='Paint', font_size=15)
        self.paint_label = CoreLabel(text='0%', font_size=15)
        self.paintDisplayBackground()
        
        #TEST
        #self._paintAirPercentage(15)
        #self._paintAirPSI(450)
        #self._paintPaint(50)
    
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
                              
            #Scope (center)
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, HUD_HEIGHT/2))
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-(HUD_HEIGHT/6)))        
            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-(HUD_HEIGHT/3)))
            
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
    
    #ASSUMES PERCENTAGE IN TERMS OF 0 - 100                 
    def _paintAirPercentage(self, percentage_full):
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
            self.air_label.text = str(percentage_full) + '%'
            self.air_label.refresh()
            texture = self.air_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(GRAPH_WIDTH + BAR_TEXT_OFFSET, HUD_HEIGHT/2), texture=texture, size=texture_size)

    #ASSUMES PSI BETWEEN 0 AND 3200    
    def _paintAirPSI(self, psi):
        with self.static_background:
            if (psi <= 1000):
                Color(1, 0, 0, mode='rgb')
            elif (psi <= 2000):
                Color(1, 1, 0, mode='rgb')
            else:
                Color(0, 1, 0, mode='rgb')
                
            level = ((100.0 - (float(psi)/float(FULL_TANK_PSI))*100.0)/100.0) * GRAPH_MAX_HEIGHT
            
            Rectangle(pos=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-level))
            
    def _paintAirPSILabel(self, psi):
        #IMPORTANT: WILL 'INHERIT' COLOR FROM LAST TIME IT WAS CHANGED
        with self.static_background:                   
            self.air_label.text = str(psi) + 'psi'
            self.air_label.refresh()
            texture = self.air_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(GRAPH_WIDTH + BAR_TEXT_OFFSET, HUD_HEIGHT/2), texture=texture, size=texture_size)
                          
    def _paintPaint(self, percentage_full):
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
            self.paint_label.text = str(percentage_full) + '%'
            self.paint_label.refresh()
            texture = self.paint_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(HUD_WIDTH - GRAPH_WIDTH - BAR_TEXT_OFFSET - 35, HUD_HEIGHT/2), texture=texture, size=texture_size)
                          
    def updateDisplay(self, data):
        for key in data:
            #print key
            if key == 'My Coords' and len(data[key]) > 0 and (data[key][0] and data[key][1]): #Correct key, not empty list, and not empty strings as members
                self.camera.setCenter(data[key][0], data[key][1])
                #print 'Camera center: ' + str(self.camera.center)
            elif key == 'My Heading':
                self.camera.setRotation(data[key])
                #print 'Camera rotation: ' + str(self.camera.rotation)
            elif key == 'Air':
                #self._paintAirPercentage(data[key]) #Uncomment for percentage of tank volume
                #self._paintAirPercentageLabel(data[key]) #Uncomment for percentage of tank volume
                self._paintAirPSI(data[key]) #Uncomment for PSI
                self._paintAirPSILabel(data[key]) #Uncomment for PSI
            elif key == 'Paint':
                self._paintPaint(data[key])
                self._paintPaintLabel(data[key])
            elif key == 'Users':
                #try:
                    print 'Users: ', data[key]
                    self._paintUsers(data[key])
                #except:
                #    print 'Could not draw user'
            else:
                print 'ScopeCanvas.updateDisplay() - Unknown key'
            
    def _paintUsers(self, users):
        for user in users:
#            print user
#            print users[user][0]
#            print users[user][1]
#            print ''
            user_coord = Point2D(users[user][0], users[user][1])
            pixel_point = geodeticToPixel(user_coord, self.camera)
            #print pixel_point
            userIcon = UserIcon(str(user), False, 0, pixel_point, users[user][2])
            userIcon.drawUserIcon(self.camera.rotation, self.static_background, 0)


if __name__ == "__main__":
    main()
