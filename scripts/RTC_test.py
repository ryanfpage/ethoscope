import smbus
import time
from ISL12026 import ISL12026

bus = smbus.SMBus(1)
myRTC= ISL12026(bus)

print hex(myRTC.getStatus())
myRTC.getDate()
