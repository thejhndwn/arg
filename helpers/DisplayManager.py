import os
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_OLED import OLED_1in51

class DisplayManager():
    def __init__(self):
        self.fontdir = os.path.dirname(os.path.realpath(__file__))

        self.disp = OLED_1in51.OLED_1in51()
        self.disp.Init()
        self.disp.clear()

    def display_text(self, text, fontsize = 12):
        self.disp.clear()
        image = Image.new('1', (self.disp.width, self.disp.height), "RED")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), fontsize)
        draw.line([(0,0),(127,0)], fill = 0)
        draw.line([(0,0),(0,63)], fill = 0)
        draw.line([(0,63),(127,63)], fill = 0)
        draw.line([(127,0),(127,63)], fill = 0)
        draw.text((20,0), text, font = font, fill = 0)

        image = image.rotate(180) 
        self.disp.ShowImage(self.disp.getbuffer(image))

    def close(self):
        self.disp.clear()
        self.disp.module_exit()
        exit()
