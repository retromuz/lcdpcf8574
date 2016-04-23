lcdpcf8574
==========

Drive a HD44780 based LCD via I²C on Raspberry Pi - with just two pins. I have used PCF8574 I²C bus expander Chip
for this purpose. This helps limited number of Raspberry Pi's pins to be better utilized. The best part is, those two pins also can be re-used because they are I²C pins, you can connect upto 127 additional devices.

Please take note that this code is based on the code posted by ufux at https://gist.github.com/ufux/6094977.

Schematics : https://raw.githubusercontent.com/karunadheera/lcdpcf8574/master/lcdpcf8574.png
           : https://raw.githubusercontent.com/karunadheera/lcdpcf8574/master/lcdpcf8574.svg

To build go to the source directory via a terminal.
$ make
$ sudo make install

That's it.

Enjoy!
