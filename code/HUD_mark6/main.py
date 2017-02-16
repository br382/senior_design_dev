# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 15:06:43 2016

@author: rick
"""

from kivy.app import App
#--SET WINDOW SIZE
from kivy.config import Config
Config.set('graphics', 'width', '428')
Config.set('graphics', 'height', '240')
#--
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock, mainthread
from Constants import *
from HUD import *
from plyer import gps

class TestApp(Label):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.hud = HUD(self.canvas)
        self.gps_status_label = CoreLabel(text='', font_size=15)
        self.gps_location_label = CoreLabel(text='', font_size=15)
        self.my_lat = 0
        self.my_lon = 0
        
    def updateDisplay(self, *args):
        print 'Inside updateDisplay'
        self.canvas.clear() #Clears canvas for fresh draw
        self.hud.scope_canvas.paintDisplayBackground() #Reinitializes the canvas with HUD background
        self.hud.work() #Retrieves data and draws appropriately on HUD background canvas
        
        #TEMPORARY label drawing for debugging purposes
        with self.canvas:
            #Display gps_location
            Color(.5, 1, 0, mode='rgb')
            self.gps_location_label.refresh()
            texture = self.gps_location_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(BAR_TEXT_OFFSET+10, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
            
            #Display gps_status
            Color(.5, 1, 0, mode='rgb')
            self.gps_status_label.refresh()
            texture = self.gps_status_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(HUD_WIDTH-BAR_TEXT_OFFSET-GRAPH_WIDTH-100, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
        
class KivyGUI(App):
    def build(self):
        self.test_app = TestApp()
        Clock.schedule_interval(self.test_app.updateDisplay, 1.0)
        self.gps = gps
        try:
            self.gps.configure(on_location=self.on_location,
                               on_status=self.on_status)
            self.gps.start()
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.test_app.gps_status_label.text = 'No GPS'
        return self.test_app
        
    @mainthread
    def on_location(self, **kwargs):
        try:
            for key in kwargs:
                if key == 'lat':
                    self.my_lat = float(kwargs[key])
                elif key == 'lon':
                    self.my_lon = float(kwargs[key])
                else:
                    pass
            self.test_app.gps_location_label.text = "lat: %s, lon: %s" % (self.my_lat, self.my_lon)
        except:
            print 'main.on_location() - Issue with grabbing lat/lon coords'

    @mainthread
    def on_status(self, stype, status):
        self.test_app.gps_status_label.text = 'type={}\n{}'.format(stype, status)
        
def main():
    KivyGUI().run()
    
if __name__ == "__main__":
    main()