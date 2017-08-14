import time, math
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI


class MQ5(object):
    SPI_PORT = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
      
    RL_value = 20                      
    RO_clean_air_factor = 6.5

    calibration_sample_times = 50
    calibration_sample_interval = 0.5
    read_sample_times = 50
    read_sample_interval = 0.005

    def __init__(self, Ro=6.5,  mq_pin=0):
        self.Ro = Ro
        self.mq_pin = mq_pin

        self.LPG = [2.3, -0.15, -0.39]
        self.CH4 = [2.3, -0.02, -0.39]

        print("Calibrating...")
        self.Ro = self.calibration(self.mq_pin)
        print('Ro: {} kOhm'.format(self.Ro))
        print('Done!')        

    def resistance_calculation(self, adc_out):
        return self.RL_value * (1023.0 - adc_out)/adc_out

    def calibration(self, mq_pin):
        value = 0
        for i in range(self.calibration_sample_times):
            value += self.resistance_calculation(self.mcp.read_adc(self.mq_pin))
            time.sleep(self.calibration_sample_interval)

        value /= self.calibration_sample_times
        value /= self.RO_clean_air_factor

        return int(value)

    def mq_read(self, mq_pin):
        Rs = 0
        for i in range(self.read_sample_times):
            Rs += self.resistance_calculation(self.mcp.read_adc(self.mq_pin))
            time.sleep(self.read_sample_interval)
        Rs /= self.read_sample_times
    
        return int(Rs)

    def get_gas_percentage(self, rs_ro_ratio, gas_id):
        if gas_id.upper() == 'LPG':
            return self.get_percentage(rs_ro_ratio, self.LPG)
        elif gas_id.upper() == 'CH4':
            return self.get_percentage(rs_ro_ratio, self.CH4)


    def get_percentage(self, rs_ro_ratio, curve):
        return int(math.pow(10, ((math.log10(rs_ro_ratio) - curve[1]) / curve[2]) + curve[0]))



if __name__ == "__main__":
    mq = MQ5()
    
    while True:
        LPG = mq.get_gas_percentage(mq.mq_read(mq.mq_pin)/mq.Ro, "LPG") # LPG concentration in the PPM unit
        CH4 = mq.get_gas_percentage(mq.mq_read(mq.mq_pin)/mq.Ro, "CH4") # LPG concentration in the PPM unit

        print("LPG: {} ppm    CH4: {} ppm".format(LPG, CH4))
        time.sleep(0.05)
