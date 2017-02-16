# -*- coding: utf-8 -*-
"""
Created on Sun May 01 13:05:23 2016

@author: rick
"""

from kivy.app import App
#--SET WINDOW SIZE
from kivy.config import Config
Config.set('graphics', 'width', '428')
Config.set('graphics', 'height', '240')
#--
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window, WindowBase
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock, mainthread
from Constants import *
from HUD import *
from plyer import gps

class TestApp(Label):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        Window.bind(on_key_down=self.onKeyDown)
        self.key_label = CoreLabel(text='', font_size=15)
        self.hud = HUD(self.canvas)
        self.gps_status_label = CoreLabel(text='', font_size=12)
        self.gps_location_label = CoreLabel(text='', font_size=12)
        self.uid_label = CoreLabel(text='UID: ', font_size=12)
        self.my_lat = 0
        self.my_lon = 0
        self.my_heading = 0
        
    def onKeyDown(self, something, keycode, text, something_else, modifiers, **kwargs):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)
        self.hud.scope_canvas.camera.setZoom(int(keycode))
        if keycode == ENTER:
            self.hud.myUID = self.hud.data.pickUID(self.hud.myUID)
            self.uid_label.text = 'UID: ' + str(self.hud.myUID)
        ###TODO: Include pickUID(keycode)        
        
    def updateDisplay(self, text):
        print 'Inside updateDisplay'
        self.hud.my_lat = self.my_lat
        self.hud.my_lon = self.my_lon
        self.hud.my_heading = self.my_heading
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
            Rectangle(pos=(BAR_TEXT_OFFSET+10, GRAPH_OFFSET_TOP_BOTTOM), texture=texture, size=texture_size)
            
            #Display UID
            Color(.5, 1, 0, mode='rgb')
            self.uid_label.refresh()
            texture = self.uid_label.texture
            texture_size = list(texture.size)
            Rectangle(pos=(HUD_WIDTH-BAR_TEXT_OFFSET-GRAPH_WIDTH-100, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
            
            #Display gps_status
#            Color(.5, 1, 0, mode='rgb')
#            self.gps_status_label.refresh()
#            texture = self.gps_status_label.texture
#            texture_size = list(texture.size)
#            Rectangle(pos=(HUD_WIDTH-BAR_TEXT_OFFSET-GRAPH_WIDTH-100, GRAPH_OFFSET_TOP_BOTTOM - 20), texture=texture, size=texture_size)
        
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
                    self.test_app.my_lat = float(kwargs[key])
                elif key == 'lon':
                    self.test_app.my_lon = float(kwargs[key])
                elif key == 'heading':
                    self.test_app.my_heading = int(kwargs[key])
                else:
                    pass
            self.test_app.gps_location_label.text = "lat: %s \n lon: %s \n heading: %s" % (self.test_app.my_lat, self.test_app.my_lon, self.test_app.my_heading)
        except:
            print 'main.on_location() - Issue with grabbing lat/lon coords'

    @mainthread
    def on_status(self, stype, status):
        self.test_app.gps_status_label.text = 'type={}\n{}'.format(stype, status)
        
def main():
    KivyGUI().run()
    
if __name__ == "__main__":
    main()