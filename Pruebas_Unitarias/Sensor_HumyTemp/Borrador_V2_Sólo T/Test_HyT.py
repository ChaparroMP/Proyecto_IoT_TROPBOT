#
#
# Test HDC_1080_ VERSION 2
#
# July 2021
#

#imports
import sys          
import time
import datetime


# Main Program

print ("")
print ("HDC_1080_ VERSION 2")
print ("")
print ("Sample uses 0x40 and SwitchDoc HDC1080 Breakout board ")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("")


import struct, array, time
from smbus import SMBus
import io, fcntl

i2c_ch=1

#I2C address of the HDC1080
HDC1080_ADDRESS =0x40 #0100 0000
I2C_SLAVE=0x0703
HDC1080_fr= 0  #Variable for read

#Register Map Pag 14 
HDC1080_TEMPERATURE_REG= 0x00
HDC1080_HUMIDITY_REG= 0x01
HDC1080_CONFIGURATION_REG= 0x02
HDC1080_MANUFACTURER_ID_REG= 0xFE
HDC1080_DEVICE_ID_REG= 0xFF
HDC1080_SERIAL_ID_FST_REG= 0xFB
HDC1080_SERIAL_ID_MID_REG= 0xFC
HDC1080_SERIAL_ID_LAST_REG= 0xFD



def read_Temperature():
    #Initialize I2C(SMBus)
    i2cbus= SMBus(i2c_ch)
    HDC1080_fr= io.open("/dev/i2c-"+str(i2c_ch), "rb", buffering=0)
    fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
    time.sleep(0.015) #15ms startup time
    
    i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x30,0x00])
    i2cbus.write_byte(HDC1080_ADDRESS,0x00)
    time.sleep(0.05)#Wait more  than 6.35ms  which is the conversion time
    
    data = HDC1080_fr.read(2) #read 2 bytes temperature data
    buf = array.array('B', data)
    
    #Read Temperature Register    
    data0=buf[0]<< 8
    data1=buf[1] 
    data_temp = data0 | data1
    
    #Convert data bytes a °C
    Temperature_data=((data_temp/(2**16))*165)- 40
    return buf,  hex(data0),  hex(data1) ,hex(data_temp),bin(data_temp), Temperature_data


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
        print (read_Temperature())
        print ("-----------------")
        time.sleep(3.0)