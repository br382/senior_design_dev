# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 19:13:11 2016

@author: rick
"""

import Tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from Constants import *
from UserIcon import *
from Storage import *
from Point2D import *
from CoordUtils import geodeticToPixel

class PaintMapUtils():
    
    def __init__(self, **kwargs):
        pass

#    def createMapView(self, image):
#        self._paintMapBackground(image)
#        self._paintScale(image)
#        self._paintUsers(image)
    
#    def _paintMapBackground(self, image):
#        image.ellipse([RING_INITIAL_OFFSET, 0, RING_INITIAL_OFFSET + SCOPE_WIDTH, HUD_HEIGHT],
#                       outline=LIME_GREEN)
#        image.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET, RING_SUBSEQUENT_OFFSET, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET],
#                       outline=LIME_GREEN)
#        image.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*2, RING_SUBSEQUENT_OFFSET*2, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*2, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*2],
#                       outline=LIME_GREEN)
#        image.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*3, RING_SUBSEQUENT_OFFSET*3, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*3, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*3],
#                       outline=LIME_GREEN)
#        center_pos = Point2D(HUD_CENTER_X, HUD_CENTER_Y)
#        staticSelfIcon = UserIcon("Me", False, 0, center_pos, 0)
#        staticSelfIcon.drawUserIcon(image)
    
    def paintScale(self, image):
        pass
    
    def paintUsers(self, users, image, camera):
        draw = ImageDraw.Draw(image)
        for user in users:
#            print user
#            print users[user][0]
#            print users[user][1]
#            print ''
            user_coord = Point2D(users[user][0], users[user][1])
            pixel_point = geodeticToPixel(user_coord, camera)
            #print pixel_point
            userIcon = UserIcon(str(user), False, 0, pixel_point, users[user][2])
            userIcon.drawUserIcon(draw)
            
            #print ''