'''
Simple painting tkinter app.
Also captures the drawing and predicts the value!
Derived from nikhilkumarsingh's paint program
https://gist.github.com/nikhilkumarsingh/85501ee2c3d8c0cfa9d1a27be5781f06
'''

from tkinter import *
import numpy as np
from keras.models import Sequential
from PIL import ImageGrab, Image
import time

class Paint(object):
    DEFAULT_PEN_SIZE = 15.0
    DEFAULT_COLOR = 'white'

    def __init__(self, model):
        self.root = Tk()
        self.model = model
        self.width = 285
        self.height = 280+37
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()

        self.x = (self.ws/3) - self.width/2
        self.y = (self.hs/3) - self.height/2
        
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        
        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.clear_button = Button(self.root, text='clear', command=self.clear)
        self.clear_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.go_button = Button(self.root, text='go', command=self.go)
        self.go_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='black', width=self.width, height=self.height)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def clear(self):
        self.activate_button(self.clear_button)
        self.c.create_rectangle(0, 0, self.width, self.height, fill = 'black')
        self.active_button.config(relief=RAISED)
        
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)
        self.color = 'white'

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
        
    def go(self):
        self.activate_button(self.go_button)
        xoffset = 3
        yoffset = 35
        x=self.root.winfo_rootx()+xoffset
        y=self.root.winfo_rooty()+yoffset
        
        x1=x+self.width-5
        y1=y+self.height-37
        ImageGrab.grab().crop((x, y, x1, y1)).save("capture.png")
        time.sleep(0.5)
        self.active_button.config(relief=RAISED)
        self.captureAndPredict()
        
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = 15 if self.eraser_on == False else 30
        paint_color = 'black' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        
    def captureAndPredict(self):
        jpg = Image.open("capture.png")
        temp = jpg.convert('L')
        imToUse = temp.resize((28, 28), Image.NEAREST)
        x = np.array(imToUse).astype('float32')
        x = x.reshape(1,1,28,28)
        pred = self.model.predict(x)
        print('Prediction: ', pred.argmax())
        return pred
    
if __name__ == '__main__':
    Paint(model)
