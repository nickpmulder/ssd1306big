import ssd1306big
import time

write = ssd1306big


while True:
 
    write.clear()

    write.wrap("Hello")

    time.sleep(5)
    
    
    write.clear()

    write.wrap("World")

    time.sleep(5)