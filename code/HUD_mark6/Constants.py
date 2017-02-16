# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:58:57 2016

@author: rick
"""

import math

#Conversions
DEGREES_TO_RADIANS = math.pi / 180.0
RADIANS_TO_DEGREES = 180.0 / math.pi

#Viewport Constants
HUD_WIDTH = 428
HUD_HEIGHT = 240
HUD_CENTER_X = HUD_WIDTH / 2 
HUD_CENTER_Y = HUD_HEIGHT / 2

#Air/Paint Level Indicator Constants
FULL_TANK_PSI = 3000
GRAPH_OFFSET_LEFT_RIGHT = 10
GRAPH_OFFSET_TOP_BOTTOM = 20
GRAPH_WIDTH = 20
GRAPH_MAX_HEIGHT = 200
BAR_TEXT_OFFSET = 20

#Map Display Constants
SCOPE_WIDTH = HUD_HEIGHT
SCOPE_HEIGHT = SCOPE_WIDTH
#RING_INITIAL_OFFSET = 94
#RING_SUBSEQUENT_OFFSET = 30
METERS_PER_PIXEL = 2.5 #2
MIN_SCOPE_X = HUD_CENTER_X - (HUD_HEIGHT/2)
MIN_SCOPE_Y = 0
MAX_SCOPE_X = HUD_CENTER_X + (HUD_HEIGHT/2)
MAX_SCOPE_Y = HUD_HEIGHT

#Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME_GREEN = (10, 240, 25)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#File Constants
BACKGROUND_FILE_NAME = "HUD_display.jpg"
UPDATED_FILE_NAME = "HUD_display_updated.jpg"

#Tile Constants
TILE_PIXEL_WD_HT = 256


### Version 2 ###

##Conversions
#DEGREES_TO_RADIANS = math.pi / 180.0
#RADIANS_TO_DEGREES = 180.0 / math.pi
#
##Viewport Constants
#HUD_WIDTH = 428 #428
#HUD_HEIGHT = 240 #240
#HUD_CENTER_X = HUD_WIDTH / 2 
#HUD_CENTER_Y = HUD_HEIGHT / 2
#
##Air/Paint Level Indicator Constants
#FULL_TANK_PSI = 3000
#GRAPH_OFFSET_LEFT_RIGHT = 10
#GRAPH_OFFSET_TOP_BOTTOM = 40
#GRAPH_WIDTH = 20
#GRAPH_MAX_HEIGHT = HUD_HEIGHT - GRAPH_OFFSET_TOP_BOTTOM*2
#BAR_TEXT_OFFSET = 5
#
##Map Display Constants
#SCOPE_WIDTH = HUD_HEIGHT
#SCOPE_HEIGHT = SCOPE_WIDTH
#METERS_PER_PIXEL = SCOPE_WIDTH / 500.0
#RING_INITIAL_OFFSET = HUD_CENTER_X - (SCOPE_WIDTH/2)
#RING_SUBSEQUENT_OFFSET = (SCOPE_WIDTH / 2) / 3
#
##Color Constants
#BLACK = (0, 0, 0)
#WHITE = (255, 255, 255)
#LIME_GREEN = (10, 240, 25)
#GREEN = (0, 255, 0)
#YELLOW = (255, 255, 0)
#RED = (255, 0, 0)
#
##Text Constants
#HEADING_LABEL_OFFSET = HUD_WIDTH / 8
#SCALE_LABEL_OFFSET = HUD_WIDTH / 6
#AIR_LABEL_OFFSET = 15
#PAINT_LABEL_OFFSET = 35
#
##File Constants
#BACKGROUND_FILE_NAME = "HUD_display.jpg"
#UPDATED_FILE_NAME = "HUD_display_updated.jpg"
#
##Tile Constants
#TILE_PIXEL_WD_HT = 256