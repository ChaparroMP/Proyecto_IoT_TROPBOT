
## Ruler 1         2         3         4         5         6         7        */

#LTR390_Lib.py ****************************************************************/
##                                                                            */
##   ┌────┐ ┌────┐                    SENSOR ALS Y UV                         */
##   └┐  ┌┘ └┐╔══╧═╗                      LTR 390                             */
##    │  │   │╚╗  ╔╝                                                          */
##    │  │   │ ║  ║       This code was designed in order to create           */
##    │  │   │ ║  ║       functions based on datasheet of LTR390 for hability */
##    │╔═╧══╗│ ║  ║       Ambient Light and UV sensor.                        */
##    │╚╗  ╔╝┘ ║  ║                                                           */
##    └┐║  ╚╗ ╔╝  ║       DEVELOPED BY: Castillo Lorena, Chaparro             */
##     └╚╗  ╚═╝  ╔╝                     Ma. del Pilar & Varón Jelitza         */
##      └╚╗     ╔╝                                                            */
##        ╚═════╝         Bogota, D.C., August  14th, 2021.                   */
##                                                                            */
##          Copyright (C) Departament de Electronics                          */
##                        School of Engineering                               */
##                        Pontificia Universidad Javeriana                    */
##                        Bogota - Colombia - South America                   */
##                                                                            */
##*****************************************************************************/

#Datasheet:https://optoelectronics.liteon.com/upload/download/DS86-2015-0004/LTR-390UV_Final_%20DS_V1%201.pdf 

# --------------------- Inclusion of Standard Headers ----------------------##
import struct, array, time
from  smbus import SMBus


#Address of LTR-390 sensor
LTR390_ADDRESS =0x53


#Define registers values from datasheets LTR 390
MAIN_CTRL = 0x00 #Control operation modes UVS/ALS 
ALS_UVS_MEAS_RATE= 0x04 #Control mesurament resolution
ALS_UVS_GAIN = 0x05
PART_ID = 0x06
MAIN_STATUS = 0x07
ALS_DATA_0 = 0x0D
ALS_DATA_1 = 0x0E
ALS_DATA_2 = 0x0F
UVS_DATA_0 = 0x10
UVS_DATA_1 = 0x11
UVS_DATA_2 = 0x12
INT_CFG = 0x19
INT_PST = 0x1A
ALS_UVS_THRES_UP_0 = 0x21
ALS_UVS_THRES_UP_1 = 0x22
ALS_UVS_THRES_UP_2 = 0x23
ALS_UVS_THRES_LOW_0 = 0x24
ALS_UVS_THRES_LOW_1 = 0x25
ALS_UVS_THRES_LOW_2 = 0x26



class Sensor_LTR390:

    #Define public functions


##FN############################################################################
#
#   read_ambient_light();
#
#   Return:  Ambiente Light data in Lux
#
#   Purpose: Obtain the ambient light value of sensor LTR390
#
#   Plan
#           Part 1: Initialize I2C channel for start communication and  
#                   Configure the "MAIN_CTRL_Register" follow datasheet
#                   for acquire only ALS value.
#           Part 2: Write ALS_UVS_MEAS_RATE with max resolution 20 bits,
#                   with a measurement rate of 25ms and Gain of 3. 
#           Part 3: Check MAIN_STATUS register, wait until bit 4 reports 
#                   that the data is ready, put Light Sensor in  standby
#                   and stop I2C communication.
#           Part 4: Use the data conversion function to pass these bits 
#                   to lux, taking into account the byte with the most
#                   significant values.  
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.14    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def read_ambient_light():
        adq_ready=0

        #* Part 1: Initialize I2C channel for start communication  and 
        #          Configure the "MAIN_CTRL_Register" follow datasheet
        #          for acquire only ALS value.
        i2cbus= SMBus(1)
        i2cbus.write_byte_data(LTR390_ADDRESS,MAIN_CTRL,0x02) 
        time.sleep(0.01) #10ms Wakeup Time from Standby

        #* Part 2: Write ALS_UVS_MEAS_RATE with max resolution 20 bits,
        #          with a measurement rate of 25ms and Gain of 3. 
        i2cbus.write_byte_data(LTR390_ADDRESS,ALS_UVS_MEAS_RATE,0x00)  
        i2cbus.write_byte_data(LTR390_ADDRESS,ALS_UVS_GAIN ,0x01) 
        time.sleep(0.4) #400ms  Convertion time

        #* Part 3:  Check MAIN_STATUS register, wait until bit 4 reports 
        #           that the data is ready, put Light Sensor in  standby
        #           and stop I2C communication.
        while adq_ready==0:
            r_main_status = i2cbus.read_byte_data(LTR390_ADDRESS,MAIN_STATUS)
            if r_main_status == 8: #search masking bits
                data_0 = i2cbus.read_byte_data(LTR390_ADDRESS,ALS_DATA_0)
                data_1 = i2cbus.read_byte_data(LTR390_ADDRESS,ALS_DATA_1)
                data_2 = i2cbus.read_byte_data(LTR390_ADDRESS,ALS_DATA_2)
                adq_ready=1
        i2cbus.write_byte_data(LTR390_ADDRESS,MAIN_CTRL,0x00)
        i2cbus.close() 

        #*  Part 4: Use the data conversion function to pass these bits 
        #           to lux, taking into account the byte with the most
        #           significant values.       
        data_amb=(data_2*65536)+(data_1*256)+data_0
        ambient_l = (0.6*data_amb)/(3*4)
        return ambient_l




##FN############################################################################
#
#   read_radiation_UV();
#
#   Return:  Ultraviolet light data in [nW/cm^2]
#
#   Purpose: Obtain the Ultraviolet light value of sensor LTR390
#
#   Plan
#           Part 1: Initialize I2C channel for start communication and  
#                   Configure the "MAIN_CTRL_Register" follow datasheet
#                   for acquire only UV value.
#           Part 2: Write ALS_UVS_MEAS_RATE with max resolution 20 bits,
#                   with a measurement rate of 25ms and Gain of 18.
#           Part 3: Check MAIN_STATUS register, wait until bit 4 reports 
#                   that the data is ready, put Light Sensor in  standby
#                   and stop I2C communication.
#           Part 4: Use the data conversion function to pass these bits 
#                   to [uW/cm^2], taking into account the byte with the most
#                   significant values.  
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.14   L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def read_radiation_UV():
        adq_ready=0

        #* Part 1: Initialize I2C channel for start communication  and 
        #          Configure the "MAIN_CTRL_Register" follow datasheet
        #          for acquire only UV value.
        i2cbus= SMBus(1)
        i2cbus.write_byte_data(LTR390_ADDRESS,MAIN_CTRL,0x0A) 
        time.sleep(0.01) #10ms Wakeup Time from Standby

        #* Part 2: Write ALS_UVS_MEAS_RATE with max resolution 20 bits,
        #          with a measurement rate of 25ms and Gain of 18. 
        i2cbus.write_byte_data(LTR390_ADDRESS,ALS_UVS_MEAS_RATE,0x00)   
        i2cbus.write_byte_data(LTR390_ADDRESS,ALS_UVS_GAIN ,0x04) 
        time.sleep(0.4) #400ms  Convertion time

        #* Part 3:  Check MAIN_STATUS register, wait until bit 4 reports 
        #           that the data is ready, put Light Sensor in  standby
        #           and stop I2C communication.
        while adq_ready==0:
            r_main_status = i2cbus.read_byte_data(LTR390_ADDRESS,MAIN_STATUS)
            if r_main_status == 8: #search masking bits
                data_0 = i2cbus.read_byte_data(LTR390_ADDRESS,UVS_DATA_0)
                data_1 = i2cbus.read_byte_data(LTR390_ADDRESS,UVS_DATA_1)
                data_2 = i2cbus.read_byte_data(LTR390_ADDRESS,UVS_DATA_2)
                adq_ready=1
        i2cbus.write_byte_data(LTR390_ADDRESS,MAIN_CTRL,0x00)
        i2cbus.close() 

        #*  Part 4: Use the data conversion function to pass these bits 
        #           to [uW/cm^2], taking into account the byte with the most
        #           significant values. WITH A  
        #            UV Sensitivity =2300 (Datasheet Pág. 7)    
        data_rad=(data_2*65536)+(data_1*256)+data_0
        radiation = (data_rad)/2300 #[uW/cm^2]
        radiation = radiation*1000 #[nW/cm^2]
        return radiation




