"""
Class to talk to the HIH6130 humidity and temperature sensor using I2C protocol.

Note that it requires a modified version of easyi2c with a write_quick() method. This
should have been given to you along with this file.
"""
import time
import easyi2c

__author__    = "Paolo Baesso, Mark Grimes"
__copyright__ = "Copyright 2017, Rymapt Ltd"
__license__   = "MIT"
# MIT licence is available at https://opensource.org/licenses/MIT

class HIH6130:
    def __init__(self, easybus=None):
        if easybus:
            self.easyi2c = easybus
            return

        DEVICE_ADDRESS = 0x27      #7 bit address (will be left shifted to add the read write bit)
        # Figure out which bus to use by seeing what devices are present
        import os
        if os.path.exists("/dev/i2c-0"):
            I2C_BUS = 0
        elif os.path.exists("/dev/i2c-1"):
            I2C_BUS = 1
        else:
            raise Exception("HIH6130: can't access the I2C bus on either '/dev/i2c-0' or '/dev/i2c-1'. Have you enabled I2C in the kernel?")

        self.easyi2c = easyi2c.IIC(DEVICE_ADDRESS, I2C_BUS)

    def __refreshData(self):
        # Perform a write operation, with no register or data, to tell the HIH6130
        # to refresh the temperature and pressure reading.
        self.easyi2c.write_quick()
        # Conversion time is ~37 ms. Pause the code to ensure new data is ready.
        time.sleep(0.1)

    def __readData(self):
        # Use  easyi2c function to read 4 chars from the HIH6130 with no specification
        # of address.
        myData= self.easyi2c.read(4)
        return myData

    def __parseData(self, myData):
        # Convert the read data to extract  status bit, humidty and temperature.
        # Return a list with [status, humidity, temperature]

        # Status bit
        # 0= normal, 1= stale data, 2= device in command mode, 3= not used
        statusBits= (myData[0] & 0xC0) >> 6
        # print 'Status bits', statusBits
        MSBhum= myData[0] & 0x3F

        # Humidity data, 14 bits. 0x0000= 0%, 0x3FFF= 100%
        humidityCount= (MSBhum << 8) | myData[1]
        RHhumidity= 100*float(humidityCount)/(pow(2,14)-2)
        # print 'Humidity count= ', humidityCount, ' %RH= ', RHhumidity

        # Temperature data, 14 bits. 0x0000= -40 C, 0x3FFF= 125 C
        temperatureCount= ((myData[2] << 8) | myData[3]) >> 2
        degTemperature= (165*float(temperatureCount)/(pow(2,14)-2))-40
        # print 'Temperature count= ', temperatureCount, ' T= ', degTemperature
        outList= [statusBits, RHhumidity, degTemperature]

        return outList

    def getData(self):
        # Forces the device to refresh its data, parses the data and returns the values in a list.
        self.__refreshData()
        outList= self.__parseData(self.__readData())
        return outList
