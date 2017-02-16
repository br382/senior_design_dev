# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12:22:15 2016

@author: rick
"""

from Tkinter import *
from HUD import *
from Constants import *
from PIL import Image, ImageTk

class HUDWindow():
    
    def __init__(self, main):
        #print 'In HUDWindow() __init__'
        #Create HUD background screen
        self.hud = HUD()
        self.main = main
        
        #Create canvas on which HUD image will be drawn and load basic image
        self.canvas = Canvas(self.main, width=HUD_WIDTH, height=HUD_HEIGHT)
        self.canvas.grid(row=0, column=0)
        self.image = ImageTk.PhotoImage(self.hud.scope_canvas.display_image)
        self.canvas_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image)
        
        #Call redraw initially
        self.main.after(1000, self.redraw)
        
    def redraw(self):
        #print 'In HUDWindow() redraw'
        #TEMP
        #END TEMP
        #Create updated HUD image according to current data
        self.hud.work()
        redraw_image = ImageTk.PhotoImage(self.hud.scope_canvas.display_image)
        self.canvas.itemconfig(self.canvas_image, image=redraw_image)
        
        #Hang onto new image to avoid garbage collector
        self.image = redraw_image
        
        #Call redraw after delay
        self.main.after(100, self.redraw)
