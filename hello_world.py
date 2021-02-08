import ssd1306big
import time

# The default wiring is SDA to GP8 and SCL to GP9 for Rasberry Pi Pico
# currently only 128x64 px display is supported. 

write = ssd1306big


while True:
 
    write.clear()

    write.wrap("Hello")

    time.sleep(5)
    
    
    write.clear()

    write.wrap("World")

    time.sleep(5)
