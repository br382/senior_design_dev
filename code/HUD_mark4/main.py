# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 17:02:52 2016

@author: rick
"""

from kivy.app import App
#--SET WINDOW SIZE
from kivy.config import Config
Config.set('graphics', 'width', '428')
Config.set('graphics', 'height', '240')
#--
from kivy.uix.label import Label
from kivy.clock import Clock
from Constants import *
from HUD import *
from random import randint

class TestApp(Label):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.hud = HUD(self.canvas)
        
    def updateDisplay(self, *args):
        print 'Inside updateDisplay'
        self.canvas.clear() #Clears canvas for fresh draw
        #self.clear_widgets() #Needed?
        #self.hud = HUD(self.canvas) #Original
        self.hud.scope_canvas.paintDisplayBackground() #Reinitializes the canvas with HUD background
        self.hud.work() #Retrieves data and draws appropriately on HUD background canvas
        
        #TEST LABELLING
        #label = Label(text='Hello', pos=(randint(0,428), randint(0,240)), size=(50,20))
        #self.add_widget(label)
        
class KivyGUI(App):
    def build(self):
        test_app = TestApp()
        Clock.schedule_interval(test_app.updateDisplay, 1.0)
        return test_app
        
def main():
    KivyGUI().run()
    
if __name__ == "__main__":
    main()