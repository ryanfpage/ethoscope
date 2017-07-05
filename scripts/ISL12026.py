import smbus
import time

# Class to talk to the ISL1206 RTC using I2C protocol.
# Written by P. Baesso - RYMAPT LTD

class ISL12026:
# Define the SMBus interface
	def __init__(self, bus):
		#bus = smbus.SMBus(1)
		DEVICE_ADDRESS = 0x6F      #7 bit address (will be left shifted to add the read write bit)
	
	def get_bit(byteval,idx):
		return ((byteval&(1<<idx))!=0);
	
	def getReg(self, regAdd):
		bus.write_byte_data(DEVICE_ADDRESS, 0x00, regAdd)
		myData = bus.read_byte(DEVICE_ADDRESS)
		return myData
		
	def setReg(self, regAdd, regData):
		sendChar=[]
		sendChar.append(regAdd)
		sendChar.append(regData)
		
		bus.write_i2c_block_data(DEVICE_ADDRESS,0x00,[0x3F, 0x02]) #write 0x02 to SR to set WEL
		bus.write_i2c_block_data(DEVICE_ADDRESS,0x00,[0x3F, 0x06]) #write 0x06 to SR to set WEL and RWEL
		bus.write_i2c_block_data(DEVICE_ADDRESS,0x00,sendChar)
		
	def getStatus(self):
		statusReg= self.getReg(0x37)
		return statusReg