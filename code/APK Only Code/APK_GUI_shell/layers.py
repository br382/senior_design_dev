from PIL import Image, ImageDraw
from random import randint


CLEAR      = (0,    0,  0,   0) #RGBA tuple constant
BLACK      = (0,    0,  0, 255)
LIME_GREEN = (10, 240, 25, 255)
RED        = (255,  0,  0, 255)

def drawStatic(res):
    img = Image.new('RGBA', res, BLACK)
    draw = ImageDraw.Draw(img)
    scale = 0.1    
    size  = [0, 0, res[0]*scale, res[1]*scale]
    r    = [randint(0, res[0]), randint(0, res[1])]
    pos  = [(size[0]+r[0], size[1]+r[1]), (size[2]+r[0], size[3]+r[1])]
    draw.rectangle(pos, fill=None, outline=LIME_GREEN)
    return img

def drawRefresh(res):
    img = Image.new('RGBA', res, CLEAR)
    draw = ImageDraw.Draw(img)
    scale = 0.1    
    size  = [0, 0, res[0]*scale, res[1]*scale]
    r    = [randint(0, res[0]), randint(0, res[1])]
    pos  = [(size[0]+r[0], size[1]+r[1]), (size[2]+r[0], size[3]+r[1])]
    draw.rectangle(pos, fill=None, outline=RED)
    return img

class layers():
    def __init__(self, x=500, y=500, static=1, dynamic=1):
        self.res       = (x,y)
        self.static    = static
        self.dynamic   = dynamic
        self.layers    = []
        self.composite = None
        for i in range(self.static):
            self._drawInit(i)
            self.layers[i] = drawStatic(self.res)
    def _image(self, bg):
        img = Image.new('RGBA', self.res, bg)
        return img
    def _merge(self, img1, img2):
        img = Image.new('RGBA', self.res, CLEAR)
        img.paste(img1, img1)
        img.paste(img2, img2)
        return img
    def _drawInit(self, ind):
        while len(self.layers)<=ind: self.layers.append(None)
        self.layers[ind] = self._image(CLEAR)
    def _compoundImages(self):
        self.composite = self._image(CLEAR)
        for i in range(len(self.layers)):
            if self.layers[i] != None:
                self.composite = self._merge(self.composite, self.layers[i])
        return
    def log(self, filename, DEBUG=True):
        try:
            self.composite.save(filename)
        except:
            if DEBUG: print 'Unable to Save: ', filename
    def refresh(self):
        for i in range(self.static + self.dynamic):
            if i >= self.static:
                self._drawInit(i)
                self.layers[i] = drawRefresh(self.res)
        self._compoundImages() 
        self.log('layers.png')
        return self.composite
        
if __name__ == '__main__':
    from time import sleep
    l = layers()
    while(1):
        try:
            sleep(1)
        except:
            break
        l.refresh()
