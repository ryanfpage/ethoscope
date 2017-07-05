import smbus
import time

# Class to talk to the ISL1206 RTC using I2C protocol.
# Written by P. Baesso - RYMAPT LTD

class ISL12026:
# Define the SMBus interface
	def __init__(self, bus):
		#bus = smbus.SMBus(1)
		self.bus= bus
		self.DEVICE_ADDRESS = 0x6F      #7 bit address (will be left shifted to add the read write bit)
		self.DATE_LIST= ['SEC', 'MIN', 'HR', 'DATE', 'MONTH', 'YR', 'DAY', 'Y2K']
	
	
	def __parseDate(self, datetimeList):
		formattedTimestamp=[-1, -1, -1, -1, -1, -1]
		#for index, iValue in enumerate(datetimeList):
		#	if (index == 2) :
		#		iValue= self.__parseHour(iValue)
		#	print self.DATE_LIST[index], self.__parseReg(iValue)
		formattedTimestamp[5]= self.__parseReg(datetimeList[0])
		formattedTimestamp[4]= self.__parseReg(datetimeList[1])
		formattedTimestamp[3]= self.__parseHour(datetimeList[2])
		formattedTimestamp[2]= self.__parseReg(datetimeList[3])
		formattedTimestamp[1]= self.__parseReg(datetimeList[4])
		formattedTimestamp[0]= 100*(self.__parseReg(datetimeList[7])) + (self.__parseReg(datetimeList[5]))
		return formattedTimestamp
		
	def __parseReg(self, inChar):
		units= inChar & 0x0F
		decs= ((inChar & 0xF0) >> 4)*10
		outValue= units+decs
		return outValue
	
		
	def __parseHour(self, inChar):
		if (self.__get_bit(inChar, 7)):
			#print "24h time"
			outChar= inChar & 0x7F
			outChar= self.__parseReg(outChar)
		else:
			#print "12h time"
			if (self.__get_bit(inChar, 5)):
				outChar= 12
				#print "PM"
			else:
				outChar=0
				#print "AM"
			inChar = inChar & 0x1F
			inChar= self.__parseReg(inChar)
			outChar= outChar+ inChar
		return outChar
	
			
	def __get_bit(self, byteval,idx):
		return ((byteval&(1<<idx))!=0);
	
	
	def getReg(self, regAdd):
		self.bus.write_byte_data(self.DEVICE_ADDRESS, 0x00, regAdd)
		myData = self.bus.read_byte(self.DEVICE_ADDRESS)
		return myData
	
		
	def setReg(self, regAdd, regData):
		sendChar=[]
		sendChar.append(regAdd)
		sendChar.append(regData)
		
		self.bus.write_i2c_block_data(self.DEVICE_ADDRESS,0x00,[0x3F, 0x02]) #write 0x02 to SR to set WEL
		self.bus.write_i2c_block_data(self.DEVICE_ADDRESS,0x00,[0x3F, 0x06]) #write 0x06 to SR to set WEL and RWEL
		self.bus.write_i2c_block_data(self.DEVICE_ADDRESS,0x00,sendChar)
	
		
	def getStatus(self):
		statusReg= self.getReg(0x3F)
		return statusReg
	
		
	def getDate(self):
		myDateTime=[]
		for iData in range(0,8):
			self.bus.write_byte_data(self.DEVICE_ADDRESS, 0x00, 0x30+iData) # the 0x00, 0x00 is the '16 bit' address split into 2 bytes
			myData = self.bus.read_byte(self.DEVICE_ADDRESS) # this will read at the current address pointer, which we on the previous line
			myDateTime.append(myData)
			#print self.DATE_LIST[iData], self.__parseReg(myData)
		formattedTimestamp= self.__parseDate(myDateTime)
		return formattedTimestamp
		
