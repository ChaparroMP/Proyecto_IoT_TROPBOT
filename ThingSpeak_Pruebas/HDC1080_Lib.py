## Ruler 1         2         3         4         5         6         7        */

#HDC1080_Lib.py **************************************************************/
##                                                                            */
##   ┌────┐ ┌────┐                    SENSOR TEMP & HUM                       */
##   └┐  ┌┘ └┐╔══╧═╗                      HDC 1080                            */
##    │  │   │╚╗  ╔╝                                                          */
##    │  │   │ ║  ║       This code was designed in order to create           */
##    │  │   │ ║  ║       functions based on datasheet of HDC1080 for hability*/
##    │╔═╧══╗│ ║  ║       sensor of humidity and temperature.                 */
##    │╚╗  ╔╝┘ ║  ║                                                           */
##    └┐║  ╚╗ ╔╝  ║       DEVELOPED BY: Castillo Lorena, Chaparro             */
##     └╚╗  ╚═╝  ╔╝                     Ma. del Pilar & Varón Jelitza         */
##      └╚╗     ╔╝                                                            */
##        ╚═════╝         Bogota, D.C., August  3rd, 2021.                    */
##                                                                            */
##          Copyright (C) Departament de Electronics                          */
##                        School of Engineering                               */
##                        Pontificia Universidad Javeriana                    */
##                        Bogota - Colombia - South America                   */
##                                                                            */
##*****************************************************************************/

#Code Reference:https://github.com/switchdoclabs/SDL_Pi_HDC1000
#Datasheet:https://www.ti.com/lit/ds/symlink/hdc1080.pdf

# --------------------- Inclusion of Standard Headers ----------------------##
import struct, array, time
from smbus import SMBus
import io, fcntl


#I2C address of the HDC1080
HDC1080_ADDRESS =0x40 #0100 0000
I2C_SLAVE=0x0703
#Variable for read
HDC1080_fr= 0  

#Register Map // Pag 14 Datasheet
HDC1080_TEMPERATURE_REG      = 0x00
HDC1080_HUMIDITY_REG         = 0x01
HDC1080_CONFIGURATION_REG    = 0x02
HDC1080_MANUFACTURER_ID_REG  = 0xFE
HDC1080_DEVICE_ID_REG        = 0xFF
HDC1080_SERIAL_ID_FST_REG    = 0xFB
HDC1080_SERIAL_ID_MID_REG    = 0xFC
HDC1080_SERIAL_ID_LAST_REG   = 0xFD

i2c_ch=1 #Channel for I2C


class Sensor_HDC1080:

    #Define public functions


##FN############################################################################
#
#   read_Temperature( );
#
#   Return:  Temperature data in ºC 
#
#   Purpose: Obtain the temperature value of sensor HDC1080
#
#   Plan
#           Part 1: Initialize I2C channel for start communication
#           Part 2: Configure the "Configuration Register" follow 
#                   datasheet for acquire only temperature value with 
#                   a resolution of  14 bits and wait the convetion time.
#           Part 3: Read 2 bytes which are the value temperature, fit the 
#                   value in an array to modify it and stop I2C communication.
#           Part 4: Use the data conversion function to pass these bits 
#                   to ºC, taking into account the byte with the most
#                   significant values. 
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.03    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def read_Temperature():

        #* Part 1: Initialize I2C channel for start communication */
        i2cbus= SMBus(i2c_ch)
        HDC1080_fr= io.open("/dev/i2c-"+str(i2c_ch), "rb", buffering=0)
        fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
        time.sleep(0.015) #15ms startup time

        #* Part 2: Configure the "Configuration Register" follow datasheet
        #          for acquire only temperature value with a resolution of 14 bits.
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x00,0x00])
        i2cbus.write_byte(HDC1080_ADDRESS,HDC1080_TEMPERATURE_REG)
        time.sleep(0.014)#Wait more than 6.35ms which is the conversion time
        
        #* Part 3: Read 2 bytes which are the value temperature, fit the 
        #          value in an array to modify it and stop I2C communication.
        data = HDC1080_fr.read(2) 
        buf = array.array('B', data)
        i2cbus.close()

        #*  Part 4: Use the data conversion function to pass these bits 
        #           to ºC, taking into account the byte with the most
        #           significant values.
        data_temp = ((buf[0]<< 8) | (buf[1])) 
        
        Temperature_data=((data_temp/(2**16))*165)- 40 #Convert data bytes a °C

        return Temperature_data


##FN############################################################################
#
#   read_Humidity()
#
#   Return:  Humidity data in %
#
#   Purpose: Obtain the humidity value of sensor HDC1080
#
#   Plan
#           Part 1: Initialize I2C channel for start communication
#           Part 2: Configure the "Configuration Register" follow 
#                   datasheet for acquire only humidity value with 
#                   a resolution of  14 bits and wait the convetion time.
#           Part 3: Read 2 bytes which are the value humidity fit the 
#                   value in an array to modify it and stop I2C communication.
#           Part 4: Use the data conversion function to pass these bits 
#                   to %, taking into account the byte with the most
#                   significant values. 
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.03    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/

    def read_Humidity():
        #* Part 1: Initialize I2C channel for start communication */
        i2cbus= SMBus(i2c_ch)
        HDC1080_fr= io.open("/dev/i2c-"+str(i2c_ch), "rb", buffering=0)
        fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
        time.sleep(0.015) #15ms startup time
        
        #* Part 2: Configure the "Configuration Register" follow datasheet
        #          for acquire only humidity value with a resolution of 14 bits.
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x00,0x00])
        i2cbus.write_byte(HDC1080_ADDRESS,HDC1080_HUMIDITY_REG)
        time.sleep(0.016) #Wait more than 6.5ms which is the conversion time
        
        #* Part 3: Read 2 bytes which are the value humidity, fit the 
        #          value in an array to modify it and stop I2C communication.
        data = HDC1080_fr.read(2) 
        buf = array.array('B', data)
        i2cbus.close()

        #*  Part 4: Use the data conversion function to pass these bits 
        #           to %, taking into account the byte with the most
        #           significant values.
        data_temp = ((buf[0]<< 8) | (buf[1]))
        Humidity_data=((data_temp/(2**16))*100) #Convert data bytes a %

        return Humidity_data


##FN############################################################################
#
#   Turn_ON_Heater( );
#
#   Return:  None
#
#   Purpose: Turn On the Heater when the Humidity value is around to 85%
#
#   Plan
#           Part 1: Initialize I2C channel for start communication
#           Part 2: Configure the "Configuration Register" follow 
#                   datasheet for Turn ON the HEATER and STOP I2C..
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.03    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def Turn_ON_Heater():

        #* Part 1: Initialize I2C channel for start communication */
        i2cbus= SMBus(i2c_ch)

        #* Part 2: Configure the "Configuration Register" follow 
        #          datasheet for Turn ON the HEATER and STOP I2C.
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x20,0x00])
        time.sleep(0.015)
        i2cbus.close()

        return 

##FN############################################################################
#
#   Turn_OFF_Heater( );
#
#   Return:  None
#
#   Purpose: Turn Off the Heater when the Humidity value is less than 85%
#
#   Plan
#           Part 1: Initialize I2C channel for start communication
#           Part 2: Configure the "Configuration Register" follow 
#                   datasheet for Turn OFF the HEATER and STOP I2C.
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.03    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def Turn_OFF_Heater():

        #* Part 1: Initialize I2C channel for start communication */
        i2cbus= SMBus(i2c_ch)

        #* Part 2: Configure the "Configuration Register" follow 
        #          datasheet for Turn OFF the HEATER and STOP I2C.
        i2cbus.write_i2c_block_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REG, [0x00,0x00])
        time.sleep(0.015)
        i2cbus.close()

        return 
