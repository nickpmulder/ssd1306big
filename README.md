# ssd1603big — i2c oled driver for micropython  
A font for micropython on 128x64 pixel ssd1306 oled display. 

Adapted from ssd1306.py micropython module. 

Rasberry Pi Pico default connections: SDA to GP8 and SCL to GP9.

This is a driver for ssd1306 i2c oled displays using micropython. It was written for a Raspberry Pi Pico but should work on any microcontroller running micropython. It was based originally on the ssd1306.py module, but a new, larger font was drawn using framebuffer lines by Nick Mulder. This module is open source, and can be used for free for any purpose. 

![example photo A through X](https://github.com/nickpmulder/ssd1306big/blob/main/a-x.jpg)
![example photo Y, Z, numbers and punctuation](https://github.com/nickpmulder/ssd1306big/blob/main/y-.jpg)
