from sensors_display import sensors_display
from sensors import *
while True:
    time.sleep(0.1)
    lumi,temp,humi=sensors(8,9)
    print(lumi,temp,humi)
    sensors_display(8, 9, lumi, temp, humi, 0)
    time.sleep(5)
    #deepsleep(10*1000)

