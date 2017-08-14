import RPi.GPIO as GPIO
import Adafruit_DHT
import time


class DHT(object):
    data_pin = 4
    DHT_model = 11

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.IN)

    def hum_temp_output(self):
        hum, temp = Adafruit_DHT.read_retry(self.DHT_model, self.data_pin, delay_seconds=2)
        return (temp, hum)

hum = DHT()

if __name__ == "__main__":
    while True:
        if hum.hum_temp_output()[1] > 100:
            pass
        else:
            print("Temperature: {}, Humidity: {}".format(hum.hum_temp_output()[0], hum.hum_temp_output()[1]))
