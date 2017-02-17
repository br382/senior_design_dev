1. Download Virtualbox.
2. Download the Kivy VM with everything pre-installed. http://kivy.org/docs/guide/packaging-android-vm.html
3. Run: 'sudo pip install -U buildozer' (password is kivy123).
4. Run: 'buildozer init'
5. Create a main.py (from commented out code below) at $HOME.
6. Run: 'buildozer android debug' (from $HOME).
7. Copy .apk file to Android device.
8. Run .apk file on Android device.

################################
__version__ = '1.2.0'
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

class TutorialApp(App):
    def build(self):
        f = FloatLayout()
        s = Scatter()
        l = Label(text="Hello!",
                  font_size=150)

        f.add_widget(s)
        s.add_widget(l)
        return f

if __name__ == "__main__":
    TutorialApp().run()
#################################

