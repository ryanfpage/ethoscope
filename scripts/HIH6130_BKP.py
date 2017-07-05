import smbus
import time
import easyi2c

# Define the SMBus interface
bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x27      #7 bit address (will be left shifted to add the read write bit)
#DEVICE_REG_MODE1 = 0x00
#DEVICE_REG_LEDOUT0 = 0x1d

# Define the easyi2c interface (allows to do read with no address)
myDevice= easyi2c.IIC(DEVICE_ADDRESS, 1) #address and bus

# Perform a write operation with no register or data, to tell the HIH6130
# to refresh the temperature and pressure reading.
bus.write_quick(DEVICE_ADDRESS)

# Conversion time is ~37 ms. Pause the code to ensure new data is ready.
time.sleep(0.1)

# Use  easyi2c function to read 4 chars from the HIH6130 with no specification
# of address.
myData=myDevice.read(4)
#for iChar in myData:
#	print hex(iChar)

# Convert the read data to extract status bit, humidty and temperature.
# Status bit 
# 0= normal, 1= stale data, 2= device in command mode, 3= not used
statusBits= (myData[0] & 0xC0) >>6
print 'Status bits', statusBits
MSBhum= myData[0] & 0x3F

# Humidity data, 14 bits. 0x0000= 0%, 0x3FFF= 100%
humidityCount= (MSBhum << 8) | myData[1]
print 'Humidity count= ', humidityCount, ' %RH= ', 100*float(humidityCount)/(pow(2,14)-2)

# Temperature data, 14 bits. 0x0000= -40 C, 0x3FFF= 125 C
temperatureCount= ((myData[2] << 8) | myData[3]) >> 2
print 'Temperature count= ', temperatureCount, ' T= ', (165*float(temperatureCount)/(pow(2,14)-2))-40
