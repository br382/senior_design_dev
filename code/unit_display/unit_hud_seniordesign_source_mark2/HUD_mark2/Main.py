# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:58:47 2016

@author: rick
"""

from HUD import *
from Tkinter import *
from PIL import Image, ImageTk
from HUDWindow import HUDWindow
import time

#ORIGINAL (will simply  generate .jpeg files)
#def main():
#    hud = HUD()
#    while(1):
#        hud.work()
#        time.sleep(1)
        
#PROTOTYPE
root = Toplevel()
HUDWindow(root)
root.mainloop()

    
#if __name__ == "__main__":
#    main()