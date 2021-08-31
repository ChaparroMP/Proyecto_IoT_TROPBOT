#
#
# Test HDC_1080_ VERSION 3
#
# July 16, 2021
#

# Main Program
import sys          
import time
import datetime
from smbus import SMBus
import HDC1080_Test


print ("")
print ("HDC_1080_ VERSION 3")
print ("")
print ("Sample uses 0x40 and SwitchDoc HDC1080 Breakout board ")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("")



sen_hdc = HDC1080_Test.Sensor_HDC1080
HDC1080_ADDRESS =0x40 #0100 0000
HDC1080_CONFIGURATION_REG    = 0x02

i2c_ch=1

#Initialize I2C(SMBus)
i2cbus= SMBus(i2c_ch)

#Read the Config register (2bytes)
data=i2cbus.read_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG,2)
print ("Old CONFIG=", [hex(data[0]),hex(data[1])]) 

#Update the Configuration Register
i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x30,0x00])

#Read the Config register (2bytes)
data=i2cbus.read_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG,2)
print ("New CONFIG=", [hex(data[0]),hex(data[1])])

i2cbus.close()

while True:
    print ("-----------------")
    print ("Temperatura:",sen_hdc.read_Temperature(),"°C")
    print ("Humedad",sen_hdc.read_Humidity(),"%")
    print ("-----------------")
    time.sleep(3.0)