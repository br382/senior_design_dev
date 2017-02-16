from kivy.app import App
#--SET WINDOW SIZE
from kivy.config import Config
Config.set('graphics', 'width', '428')
Config.set('graphics', 'height', '240')
#--
from kivy.graphics import Color, Line, Rectangle, Triangle
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from Constants import *
from Point2D import *
from UserIcon import *
from ScopeCanvas import *

class TestApp(Label):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        #self.adjust = 25
        self.scopeCanvas = ScopeCanvas(self.canvas)
        
    def updateDisplay(self, *args):
        print 'Inside updateDisplay'
        self.canvas.clear()
        self.scopeCanvas = ScopeCanvas(self.canvas)
        #self.scopeCanvas.updateDisplay()
        
class KivyGUI(App):
    def build(self):
        test_app = TestApp()
        Clock.schedule_interval(test_app.updateDisplay, 1.0)
        return test_app
        
def main():
    KivyGUI().run()
    
if __name__ == "__main__":
    main()


#class HudApp(App):
#    def build(self):
#        layout = FloatLayout(size=(HUD_WIDTH, HUD_HEIGHT))
#        hud_canvas = Label(size_hint=(1, 1), pos=(0, 0))
#        self.adjust = 25
#        #hud_canvas = Button(text='Hello', size_hint=(1, 1), pos=(0, 0))
#        layout.add_widget(hud_canvas)
#        with hud_canvas.canvas:
#        
#            #Solid filled rectangles
#            Color(1, 1, 1, mode='rgb')
#            Line(rectangle=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM, GRAPH_WIDTH, GRAPH_MAX_HEIGHT))
#            Color(.5, 1, 0, mode='rgb')
#            Rectangle(pos=(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-25))
#            
#            #Empty rectangles
#            Color(1, 1, 1, mode='rgb')
#            Line(rectangle=(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM, GRAPH_WIDTH, GRAPH_MAX_HEIGHT))
#            
#            #Empty circles
#            Color(.5, 1, 0, mode='rgb')
#            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, HUD_HEIGHT/2))
#            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-40))        
#            Line(circle=(HUD_WIDTH/2, HUD_HEIGHT/2, (HUD_HEIGHT/2)-80))
#            
#            #Filled triangle
##            Color(.5, 1, 0, mode='rgb')
##            center_pos = Point2D(HUD_CENTER_X, HUD_CENTER_Y)
##            staticSelfIcon = UserIcon("Self", False, 0, center_pos, 0)
##            icon_coords = staticSelfIcon.drawUserIcon(0, 1)
##            triangle = ObjectProperty(None)
##            triangle = Triangle(points=[icon_coords[0][0], icon_coords[0][1], icon_coords[1][0], icon_coords[1][1], icon_coords[2][0], icon_coords[2][1]])
#            
#            #Test canvas passing (works)
#        Clock.schedule_interval(partial(testDraw, canvas=hud_canvas.canvas), 1.0) 
##        self.testDraw()            
#            
#        return layout
#        
#    def testDraw(self, canvas, dt):
#        self.adjust = self.adjust + 1
#        with canvas:
#            Color(.5, 1, 0, mode='rgb')
#            Rectangle(pos=(50, 100), size=(GRAPH_WIDTH, GRAPH_MAX_HEIGHT-self.adjust))
#
#HudApp().run()

