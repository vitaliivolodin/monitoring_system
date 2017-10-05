from Adafruit_IO import *
from dht11 import DHT11
from yl38 import YL38
import RPi.GPIO as GPIO
import time

dht = DHT11.DHT()
yl = YL38.YL38()

while True:  
    aio.send('temperature', dht.hum_temp_output()[0] - 2)
    time.sleep(1)
    if dht.hum_temp_output()[1] > 100 or dht.hum_temp_output()[1] < 0:
        pass
    else:
        aio.send('humidity', dht.hum_temp_output()[1])
        time.sleep(1)
    aio.send('soil humidity', yl.mapping())
    time.sleep(1)
