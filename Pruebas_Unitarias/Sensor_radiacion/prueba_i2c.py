
import struct, array, time
from  smbus import SMBus
import RPi.GPIO as GPIO


#Address of LT-390 sensor
LT390_ADDRESS =0x53
#import Rpi.GPIO as GPIO
#define registers values from datasheets LT 390
MAIN_CTRL = 0x00 #Control operation modes UVS/ALS 
ALS_UVS_MEAS_RATE= 0x04 #Control mesurament resolution
ALS_UVS_GAIN = 0X05
PART_ID = 0X06
MAIN_STATUS = 0X07
ALS_DATA_0 = 0X0D
ALS_DATA_1 = 0X0E
ALS_DATA_2 = 0X0F
UVS_DATA_0 = 0X10
UVS_DATA_1 = 0X11
UVS_DATA_2 = 0X12
INT_CFG = 0X19
INT_PST = 0X1A
ALS_UVS_THRES_UP_0 = 0X21
ALS_UVS_THRES_UP_1 = 0X22
ALS_UVS_THRES_UP_2 = 0X23
ALS_UVS_THRES_LOW_0 = 0X24
ALS_UVS_THRES_LOW_1 = 0X25
ALS_UVS_THRES_LOW_2 = 0X26


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(INT_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#def my_callback(channel):
#    print("Se detectó un flanco de subida")
# 
def read_ambient():
    r_main_status = i2cbus.read_byte_data(LT390_ADDRESS,MAIN_STATUS)
    if r_main_status == 8: #search masking bits
        data_0 = i2cbus.read_byte_data(LT390_ADDRESS,ALS_DATA_0)
        data_1 = i2cbus.read_byte_data(LT390_ADDRESS,ALS_DATA_1)
        data_2 = i2cbus.read_byte_data(LT390_ADDRESS,ALS_DATA_2)
        data_amb=(data_2*65536)+(data_1*256)+data_0
        ambient = (0.6*data_amb)/(3*4)
        read_main_status = i2cbus.read_byte_data(LT390_ADDRESS,MAIN_STATUS)
        print("Ambient Light = ",ambient,"[lux]")
    return ambient


def read_radiation():
    r_main_status = i2cbus.read_byte_data(LT390_ADDRESS,MAIN_STATUS)
    if r_main_status == 8: #search masking bits
        data_0 = i2cbus.read_byte_data(LT390_ADDRESS,UVS_DATA_0)
        data_1 = i2cbus.read_byte_data(LT390_ADDRESS,UVS_DATA_1)
        data_2 = i2cbus.read_byte_data(LT390_ADDRESS,UVS_DATA_2)
        data_rad=(data_2*65536)+(data_1*256)+data_0
        radiation = (data_rad)
        read_main_status = i2cbus.read_byte_data(LT390_ADDRESS,MAIN_STATUS)
        print("UV Light = ",radiation)
    return radiation

#GPIO.add_event_detect(INT_GPIO,GPIO.BOTH,callback=my_callback,bouncetime=10)

while True:
    #**********************************************************#
    #Create a SMbus Oject
    i2cbus = SMBus(1) 
    #Write MAIN_CTRL initial configuration
    i2cbus.write_byte_data(LT390_ADDRESS,MAIN_CTRL,0x02) #sensor active ALS mode
    #Write ALS_UVS_MEAS_RATE with max resolution
    i2cbus.write_byte_data(LT390_ADDRESS,ALS_UVS_MEAS_RATE,0x00)   
    #i2cbus.write_byte_data(LT390_ADDRESS,INT_CFG,0x34)
    ambient_l = read_ambient()
    #i2cbus.write_byte_data(LT390_ADDRESS,MAIN_CTRL,0x00)
    time.sleep(2.0)
    #Write MAIN_CTRL initial configuration
    i2cbus.write_byte_data(LT390_ADDRESS,MAIN_CTRL,0x0A) #sensor active UVS mod
    radiation = read_radiation()
    time.sleep(2.0)

 		
