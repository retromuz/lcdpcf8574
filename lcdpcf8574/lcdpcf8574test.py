# /*
#  *  lcdpcf8574test.py:
#  *  Python example for using I²C based PCF8574 driver for HD44780 based LCD 
#  *  to be used with wiringPi for Raspberry Pi
#  *
#  * Copyright (c) 2013 Prageeth Karunadheera. http://karunadheera.com/
#  ***********************************************************************
#  *
#  *    lcdpcf8574 is free software: you can redistribute it and/or modify
#  *    it under the terms of the GNU Lesser General Public License as published by
#  *    the Free Software Foundation, either version 3 of the License, or
#  *    (at your option) any later version.
#  *
#  *    lcdpcf8574 is distributed in the hope that it will be useful,
#  *    but WITHOUT ANY WARRANTY; without even the implied warranty of
#  *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  *    GNU Lesser General Public License for more details.
#  *
#  *    You should have received a copy of the GNU Lesser General Public License
#  *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
#  ***********************************************************************
#  */

from ctypes import cdll
from ctypes import POINTER
from ctypes import Structure
from ctypes import c_long
from ctypes import c_int
from ctypes import byref
import time


class CustomFontsStruct(Structure):
    _fields_ = [("array", (c_int * 8) * 8)]

class CustomFontStruct(Structure):
    _fields_ = [("array", c_int * 8)]


liblcdpcf8574 = cdll.LoadLibrary('./liblcdpcf8574.so')
liblcdpcf8574.lcdpcf8574_loadcustomfonts.argtypes = [POINTER(CustomFontsStruct)]
liblcdpcf8574.lcdpcf8574_loadcustomfonts.restype = None
liblcdpcf8574.lcdpcf8574_loadcustomfont.argtypes = [POINTER(CustomFontStruct), c_int]
liblcdpcf8574.lcdpcf8574_loadcustomfont.restype = None



class lcdpcf8574(object):
    def __init__(self, addr, onetimeinit=0, wait=1, backlight=0):
        self.obj = liblcdpcf8574.new_lcdpcf8574(addr, onetimeinit, wait, backlight)
            
    def loadcustomfonts(self, fonts):
        liblcdpcf8574.lcdpcf8574_loadcustomfonts(byref(fonts))

    def loadcustomfont(self, font, addr):
        liblcdpcf8574.lcdpcf8574_loadcustomfont(byref(font), c_long(addr))

    def lcd_puts(self, string, line, col):
        liblcdpcf8574.lcdpcf8574_lcd_puts(string, line, col)

    def lcd_put_custom(self, c, line, col):
        liblcdpcf8574.lcdpcf8574_lcd_put_custom(c, line, col)

    def lcd_clear(self):
        liblcdpcf8574.lcdpcf8574_lcd_clear()
        
            
 
c = lcdpcf8574(0x38, 0, 1, 1)
customfonts = [[ 0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00011111 ], 
               [ 0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00011111, 0b00011111 ], 
               [ 0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00011111, 0b00011111, 0b00011111 ],
               [ 0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00011111, 0b00011111, 0b00011111, 0b00011111 ],
               [ 0b00001110, 0b00011011, 0b00010001, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111 ],
               [ 0b00001110, 0b00011011, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111 ],
               [ 0b00001110, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111 ],
               [ 0b00001110, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111 ]]
  
fontsstruct = CustomFontsStruct()
for i in range(8):
    for j in range(8):
        fontsstruct.array[i][j] = customfonts[i][j];
  
c.loadcustomfonts(fontsstruct)
c.lcd_puts("Using               ", 0, 0)
c.lcd_puts("C++ Dynamic Linker  ", 1, 0)
c.lcd_puts("Via Python          ", 2, 0)
keyboardInterrupt = False
while not keyboardInterrupt:
    try: 
        c.lcd_put_custom(0, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(1, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(2, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(3, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(4, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(5, 0, 19)
        time.sleep(1.0)   
        c.lcd_put_custom(6, 0, 19)
        time.sleep(1.0)
        time.sleep(1.0)   
    except KeyboardInterrupt:
        keyboardInterrupt = True
c.lcd_clear()
c.lcd_puts("Quitting...         ", 0, 0)
fontstruct = CustomFontStruct()
customfont1 = [0b00011100, 0b00000100, 0b00000100, 0b00000000, 0b00011100, 0b00010100, 0b00011100, 0b00000000] 
for i in range(0,8):
    fontstruct.array[i] = customfont1[i]
c.loadcustomfont(fontstruct, 7)
c.lcd_put_custom(7, 0, 19)
fontstruct.array[7] = 0b00011111111
c.loadcustomfont(fontstruct, 6)
c.lcd_put_custom(6, 0, 18)
c.lcd_put_custom(5, 0, 17)
time.sleep(2.0)
c.lcd_clear()
