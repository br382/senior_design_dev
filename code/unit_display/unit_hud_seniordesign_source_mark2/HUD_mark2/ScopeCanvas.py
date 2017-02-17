# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:19:29 2016

@author: rick
"""
from Camera import Camera
import Tkinter as tk
from PIL import Image, ImageTk, ImageDraw
#import math
from Constants import *
from Storage import *
from PaintMapUtils import *
from UserIcon import UserIcon

HEADING = 360

def main():
    scope_canvas = ScopeCanvas()
    #display_image = Image.open("HUD_display.jpg")
    #scope_canvas._paintAirPercentage(86, display_image)
    #scope_canvas._paintAirPSI(2500, display_image)
    #scope_canvas._paintPaint(9, display_image)
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
    
    #display_image.save("HUD_display_updated.jpg")
    

class ScopeCanvas():
    
    def __init__(self, **kwargs):
        self.camera = Camera()
        self.display_image = Image.new("RGB", (HUD_WIDTH, HUD_HEIGHT), BLACK)
        self.paintMapUtils = PaintMapUtils()
        self._paintDisplayBackground()
    
###### --NEW--    
    def _paintDisplayBackground(self):
        new_display_image = self.display_image
        draw = ImageDraw.Draw(new_display_image)
        #Air (left)
        draw.rectangle([(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM),
                        (GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
                         fill=None, outline=LIME_GREEN)
                          
        #Scope (center)
        draw.ellipse([RING_INITIAL_OFFSET, 0, RING_INITIAL_OFFSET + SCOPE_WIDTH, HUD_HEIGHT],
                      outline=LIME_GREEN)
        draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET, RING_SUBSEQUENT_OFFSET, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET],
                      outline=LIME_GREEN)
        draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*2, RING_SUBSEQUENT_OFFSET*2, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*2, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*2],
                      outline=LIME_GREEN)
        draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*3, RING_SUBSEQUENT_OFFSET*3, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*3, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*3],
                      outline=LIME_GREEN)
        center_pos = Point2D(HUD_CENTER_X, HUD_CENTER_Y)
        staticSelfIcon = UserIcon("Self", False, 0, center_pos, 0)
        staticSelfIcon.drawUserIcon(self.camera.rotation, draw, 1)
        
        #Paint (right)
        draw.rectangle([(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM),
                        (HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
                         fill=None, outline=LIME_GREEN)
                         
        filename = "HUD_display.jpg"
        self.display_image.save(filename)
        
        self.display_image = new_display_image
    
    #ASSUMES PERCENTAGE IN TERMS OF 0 - 100                 
    def _paintAirPercentage(self, percentage_full, image): #, image):
        draw = ImageDraw.Draw(image)
        
        fill_color = None
        if (percentage_full <= 25):
            fill_color = RED
        elif (percentage_full <= 50):
            fill_color =  YELLOW
        else:
            fill_color = GREEN
        
        level = ((100.0 - float(percentage_full))/100.0) * GRAPH_MAX_HEIGHT
        
        draw.rectangle([(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM + level),
                        (GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
                         fill=fill_color)
                         
        draw.text((GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH + BAR_TEXT_OFFSET, GRAPH_OFFSET_TOP_BOTTOM + level), 
                  str(percentage_full) + "%", fill=fill_color)
                  
        draw.text((GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH + BAR_TEXT_OFFSET + HEADING_LABEL_OFFSET, GRAPH_OFFSET_TOP_BOTTOM), 
                  "HEADING: " + str(HEADING), fill=LIME_GREEN)
                  
        draw.text((AIR_LABEL_OFFSET, HUD_HEIGHT - GRAPH_OFFSET_TOP_BOTTOM/2), 
                  "AIR", fill=fill_color)
    
    def _paintAirPSI(self, psi, image):
        draw = ImageDraw.Draw(image)
        
        fill_color = None
        if (psi <= 1000):
            fill_color = RED
        elif (psi <= 2000):
            fill_color =  YELLOW
        else:
            fill_color = GREEN
            
        level = ((100.0 - (float(psi)/float(FULL_TANK_PSI))*100.0)/100.0) * GRAPH_MAX_HEIGHT
        
        draw.rectangle([(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM + level),
                        (GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
                         fill=fill_color)
                         
        draw.text((GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH + BAR_TEXT_OFFSET, GRAPH_OFFSET_TOP_BOTTOM + level), 
                  str(int(psi)) + "psi", fill=fill_color)
                  
        draw.text((40, 20), 
                  "HEADING: " + str(HEADING), fill=LIME_GREEN)
                  
        draw.text((AIR_LABEL_OFFSET, HUD_HEIGHT - GRAPH_OFFSET_TOP_BOTTOM/2), 
                  "AIR", fill=fill_color)
                          
    def _paintPaint(self, percentage_full, image):
        draw = ImageDraw.Draw(image)
        temp_text_offset = BAR_TEXT_OFFSET
        fill_color = None
        if (percentage_full <= 25):
            fill_color = RED
        elif (percentage_full <= 50):
            fill_color =  YELLOW
        else:
            fill_color = GREEN
            
        if (percentage_full == 100):
            temp_text_offset = temp_text_offset + 20
        elif (percentage_full > 9 and percentage_full < 100):
            temp_text_offset = temp_text_offset + 15
        else:
            temp_text_offset = temp_text_offset + 10
            
        level = ((100.0 - float(percentage_full))/100.0) * GRAPH_MAX_HEIGHT
            
        draw.rectangle([(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM + level),
                        (HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
                         fill=fill_color)
                         
        draw.text((HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH - (temp_text_offset), GRAPH_OFFSET_TOP_BOTTOM + level), 
                  str(percentage_full) + "%", fill=fill_color)
                 
        draw.text((HUD_WIDTH - 100, 20), 
                  "SCALE: 10m", fill=LIME_GREEN)
                  
        draw.text((HUD_WIDTH - PAINT_LABEL_OFFSET, HUD_HEIGHT - GRAPH_OFFSET_TOP_BOTTOM/2), 
                  "PAINT", fill=fill_color)
                          
    def updateDisplay(self, data):
        #TEMP
        new_display_image =  Image.new("RGB", (HUD_WIDTH, HUD_HEIGHT), BLACK)
        self.display_image = new_display_image
        self._paintDisplayBackground()        
        #print new_display_image
        #END TEMP
        #new_display_image = self.display_image
        for key in data:
            #print key
            if key == 'My Coords' and len(data[key]) > 0 and (data[key][0] and data[key][1]): #Correct key, not empty list, and not empty strings as members
                self.camera.setCenter(data[key][0], data[key][1])
                #print 'Camera center: ' + str(self.camera.center)
            elif key == 'My Heading':
                self.camera.setRotation(data[key])
                #print 'Camera rotation: ' + str(self.camera.rotation)
            elif key == 'Air':
                #self._paintAirPercentage(data[key], new_display_image) #Uncomment for percentage of tank volume
                self._paintAirPSI(data[key], self.display_image) #Uncomment for PSI
            elif key == 'Paint':
                self._paintPaint(data[key], self.display_image)
            elif key == 'Users':
                for user in data[key]:
                    try:
                        #self.paintMapUtils.paintUsers(data[key], self.display_image, self.camera)
                        self._paintUsers(data[key], self.display_image)
                        #print 'User: ' + str(user) + '- ' + str(data[key][user])
                    except:
                        print 'Could not draw user'
        try:
            self.display_image.save('HUD_IMAGE_hud_test.png')
            #self.display_image.save('HUD_IMAGE' + str(HEADING) + '.jpg')
            #self.display_image.save('HUD_IMAGE' + str(int(timestamp())%100) + '.jpg')
        except:
            print 'Cannot save image'
            
        #self.display_image = new_display_image
            
    def _paintUsers(self, users, image):
        draw = ImageDraw.Draw(image)
        for user in users:
#            print user
#            print users[user][0]
#            print users[user][1]
#            print ''
            user_coord = Point2D(users[user][0], users[user][1])
            pixel_point = geodeticToPixel(user_coord, self.camera)
            #print pixel_point
            userIcon = UserIcon(str(user), False, 0, pixel_point, users[user][2])
            userIcon.drawUserIcon(self.camera.rotation, draw, 0)


if __name__ == "__main__":
    main()
