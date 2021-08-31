##########################################################
#-------------------SENSOR TEMP Y HUM--------------------#
#-------------------------HDC1080------------------------#
##########################################################

#Code Reference:https://github.com/switchdoclabs/SDL_Pi_HDC1000
#Datasheet:https://www.ti.com/lit/ds/symlink/hdc1080.pdf

import struct, array, time
from smbus import SMBus
import io, fcntl

i2c_ch=1

#I2C address of the HDC1080
HDC1080_ADDRESS =0x40 #0100 0000
I2C_SLAVE=0x0703
HDC1080_fr= 0  #Variable for read

#Register Map Pag 14
HDC1080_TEMPERATURE_REG      = 0x00
HDC1080_HUMIDITY_REG         = 0x01
HDC1080_CONFIGURATION_REG    = 0x02
HDC1080_MANUFACTURER_ID_REG  = 0xFE
HDC1080_DEVICE_ID_REG        = 0xFF
HDC1080_SERIAL_ID_FST_REG    = 0xFB
HDC1080_SERIAL_ID_MID_REG    = 0xFC
HDC1080_SERIAL_ID_LAST_REG   = 0xFD

i2c_ch=1

#Put in high value '1' for READ and '0' for WRITE
class Sensor_HDC1080:
    #Define public functions
    def read_Temperature():
        #Initialize I2C(SMBus)
        i2cbus= SMBus(i2c_ch)
        HDC1080_fr= io.open("/dev/i2c-"+str(i2c_ch), "rb", buffering=0)
        fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
        time.sleep(0.015) #15ms startup time
        
        #Resolution 14bits, only Temperature adquisition
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x00,0x00])
        i2cbus.write_byte(HDC1080_ADDRESS,HDC1080_TEMPERATURE_REG)
        time.sleep(0.014)#Wait more than 6.35ms which is the conversion time
        
        data = HDC1080_fr.read(2) #read 2 bytes temperature data
        buf = array.array('B', data)
        i2cbus.close()
        
        #Read Temperature Register    
        data_temp = ((buf[0]<< 8) | (buf[1]))
        
        #Convert data bytes a °C
        Temperature_data=((data_temp/(2**16))*165)- 40
        return Temperature_data

    def read_Humidity():
        #Initialize I2C(SMBus)
        i2cbus= SMBus(i2c_ch)
        HDC1080_fr= io.open("/dev/i2c-"+str(i2c_ch), "rb", buffering=0)
        fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
        time.sleep(0.015) #15ms startup time
        
        #Resolution 14bits, only Humidity adquisition
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x00,0x00])
        i2cbus.write_byte(HDC1080_ADDRESS,HDC1080_HUMIDITY_REG)
        time.sleep(0.016) #Wait more than 6.5ms which is the conversion time
        
        data = HDC1080_fr.read(2) #read 2 bytes humidity data
        buf = array.array('B', data)
        i2cbus.close()
        
        #Read Humidity Register    
        data_temp = ((buf[0]<< 8) | (buf[1]))
        
        #Convert data bytes a %
        Humidity_data=((data_temp/(2**16))*100)
        return Humidity_data

