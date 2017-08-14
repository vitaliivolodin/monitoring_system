import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI


class YL38(object):
    SPI_PORT = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    read_times = 100
    read_interval = 0.25 

    def __init__(self, yl_pin=1):
        self.yl_pin = yl_pin

        self.min_in = 1023
        self.max_in = 0
        self.min_out = 0
        self.max_out = 45

    def mapping(self):
        return (self.mcp.read_adc(self.yl_pin) - self.min_in) * (self.max_out - self.min_out)/(self.max_in - self.min_in) + self.min_out

    def moisture(self):
        moisture = []
        counter = self.read_times
        while counter:
            moisture.append(self.mapping())
            time.sleep(self.read_interval)
            counter -= 1

        return sum(moisture) / self.read_times            

yl = YL38()
if __name__ == '__main__':
    while True:
        print('Soil moisture: {:.2f}'.format(yl.mapping()))
        time.sleep(1)
