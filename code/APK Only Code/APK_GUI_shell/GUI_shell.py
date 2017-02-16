from layers import layers
from kivy.app             import App
from kivy.config          import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image       import AsyncImage, Image
from kivy.clock           import Clock
from kivy.core.window     import Window

#RES = (428, 240)
#RES = Window.size #initial resolution
#print 'Window Resolution: ', RES
#Config.set('graphics', 'width',  RES[0])
#Config.set('graphics', 'height', RES[1])

class TestApp(FloatLayout):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.size = Window.size
        print 'Window Resolution: ', self.size
        self.lay  = layers(x=self.size[0], y=self.size[1])
        self.lay.refresh()
        self.img = AsyncImage(source='layers.png')
        self.add_widget(self.img)
    def updateDisplay(self, *args):
        if not(self.size[0] == Window.size[0]) or not(self.size[1] == Window.size[1]):
            self.size = Window.size
            self.lay  = layers(x=self.size[0], y=self.size[1])
            print 'Window Resolution: ', self.size
        self.lay.refresh()
        
class KivyGUI(App):
    def build(self):
        test_app = TestApp()
        Clock.schedule_interval(test_app.updateDisplay, 0.0)
        return test_app

def main():
    KivyGUI().run()

if __name__ == '__main__':
    main()
