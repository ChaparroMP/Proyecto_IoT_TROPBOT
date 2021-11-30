## Ruler 1         2         3         4         5         6         7        */

#GPSProxLib.py ****************************************************************/
##                                                                            */
##   ┌────┐ ┌────┐                    SENSOR Proximidad HY-SF05  y            */
##   └┐  ┌┘ └┐╔══╧═╗                     GPS  Ublox NEO-6M v2                 */
##    │  │   │╚╗  ╔╝                                                          */
##    │  │   │ ║  ║       This code was designed to create functions based on */
##    │  │   │ ║  ║       the HY-SF05 and GPS Ublox NEO-6M v2 datasheet to use*/
##    │╔═╧══╗│ ║  ║       them according to the proposed needs.               */
##    │╚╗  ╔╝┘ ║  ║                                                           */
##    └┐║  ╚╗ ╔╝  ║       DEVELOPED BY: Castillo Lorena, Chaparro             */
##     └╚╗  ╚═╝  ╔╝                     Ma. del Pilar & Varón Jelitza         */
##      └╚╗     ╔╝                                                            */
##        ╚═════╝         Bogota, D.C., August  20th, 2021.                   */
##                                                                            */
##          Copyright (C) Departament de Electronics                          */
##                        School of Engineering                               */
##                        Pontificia Universidad Javeriana                    */
##                        Bogota - Colombia - South America                   */
##                                                                            */
##*****************************************************************************/

#HY-SF05 Code Reference :https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#                        https://raspberrypi.stackexchange.com/questions/95332/ultrasonic-sensor-stops-working-a-few-minutes-later 
#HY-SF05 Datasheet:https://datasheetspdf.com/pdf-file/813041/ETC/HY-SRF05/1



#GPS  Ublox NEO-6M v2  Code Reference :https://lastminuteengineers.com/neo6m-gps-arduino-tutorial/
#                                      https://medium.com/@kekreaditya/interfacing-u-blox-neo-6m-gps-module-with-raspberry-pi-1df39f9f2eba
#GPS  Ublox NEO-6M v2  Datasheet:https://www.u-blox.com/sites/default/files/products/documents/NEO-6_DataSheet_(GPS.G6-HW-09005).pdf



# --------------------- Inclusion of Standard Headers ----------------------##
import time
from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setwarnings(False)

#GPIO Mode (BOARD/BCM)
GPIO.setmode(GPIO.BOARD) #(GPIO.BCM)


class GPS_Prox:

    #Define public functions

##FN############################################################################
#
#   conetion_GPS(data_GPS);
#
#   Return:  -----
#
#   Purpose: -----
#
#   Plan
#           Part 1: --
#           Part 2: ---
#           Part 3: ---
#           Part 4: ---- 
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.26    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def conection_GPS(data_GPS):
        if data_GPS[2:9] == "$GPRMC,":
            if ((data_GPS[8:10] == ",,") or (data_GPS[21:23] == ",,")or (data_GPS[25:27] == ",,")):
                print("No se pudo conectar con la antena ")
                return 0
            else:
                return 1
            



##FN############################################################################
#
#   sym_to_text(data);
#
#   Return:  -----
#
#   Purpose: -----
#
#   Plan
#           Part 1: --
#           Part 2: ---
#           Part 3: ---
#           Part 4: ---- 
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	Aug.26    L.Castillo,P.Chaparro     Initial implementation
#              & J. Varón
#################################################################################/
    def sym_to_text(data):
        GPS_vect_data=["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        #* Part 1: ------ */
        if data[2:9] == "$GPRMC,":
            hour = data[9:11]
            minute = data[11:13]
            second = data[13:15]
            
            local_hour = int(hour) + 19 # diferencia horaria
            if local_hour > 24:
                local_hour -=  24
            local_hour = str(local_hour)

            #-------------------------------------------------------------------------
            row1=data[18:21]
            if row1 == ",A,":
                comma=data[21:].index(",")
                lat = data[21:22+(comma)]
                deg = lat[0:2]
                minn= lat[2:4]
                sec = lat[5:7]
                mils= lat[7:]
                mils_lat=mils[1:3]
                coord = data[(21+comma+1)]
                #-------------------------------------------------------------------------
                nxtr=data.index(coord)
                row2 = data[(nxtr+1)]
                if row2 == ",":           
                    comma2 = data[(nxtr+2):].index(",")
                    lon = data[(nxtr+2):(nxtr+2+comma2)]
                    grados = lon[1:3]
                    min_l= lon[3:5]
                    sec_l  = lon[6:8]
                    mils_l = lon[8:]
                    coord_l = data[(nxtr+2)+comma2+1]
                    #-------------------------------------------------------------------------
                    nextr=data.index(coord_l)
                    row3= data[(nextr+1)]
                    if row3 == ",":
                        comma3 = data[(nextr+2):].index(",")
                        speed = data[(nextr+2):(nextr+2+comma3)]
                        comma4_5 = data[nextr+4+comma3]
                        resulting = data[nextr+4+comma3:]
                        dd = resulting[0:2]
                        mm = resulting[2:4]
                        yy = resulting[4:6]
                        #-------------------------------------------------------------------------

                        GPS_vect_data=[local_hour, minute, second, deg, minn,sec,mils_lat,coord, grados, min_l,sec_l,mils_l,coord_l,
                                    dd,mm,yy]
            return GPS_vect_data



##FN############################################################################
#
#   distance(GPIO_TRIGGER, GPIO_ECHO);
#
#   Return:  Distance in cm 
#
#   Purpose: Acquire the distance to an obstacle in cm from the HY SR05 sensor
#
#   Plan
#           Part 1: Set GPIO direction (IN/OUT)
#           Part 2: Set trigger to HIGH
#           Part 3: Set trigger after 0.01ms to LOW
#           Part 4: Save Start Time
#           Part 5: Save time of arrival
#           Part 6: Time difference between start and arrival
#           Part 7: Multiply by the sonic speed (34300 cm/s)
#                   divied by 2 because there and back
#
#
#   Register of Revisions (Debugging Process):
#
#   DATE       RESPONSIBLE  			COMMENT
#   -----------------------------------------------------------------------
# 	
#################################################################################/
    def distance(GPIO_TRIGGER, GPIO_ECHO):
        try:
            #Timeout prox
            maxTime=0.04

            #* Part 1: Set GPIO direction (IN/OUT)
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
            GPIO.output(GPIO_TRIGGER,False)
            
            time.sleep(0.01)
            
            #* Part 2: Set trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
            
            
            # Part 3:Set trigger after 0.01ms to LOW
            time.sleep(0.0001)
            GPIO.output(GPIO_TRIGGER,False)
            
            # Part 4:Save Start Time
            pulse_start=time.time()
            timeout=pulse_start + maxTime
            
            while (GPIO.input(GPIO_ECHO) == 0  and pulse_start < timeout):
                pulse_start=time.time()

            # Part 5:Save of arrival   
            pulse_end = time.time()
            timeout = pulse_end + maxTime
            
            while (GPIO.input(GPIO_ECHO) == 1 and pulse_end < timeout):
                pulse_end = time.time()
        
            # Part 6:Time difference between start and arrival
            pulse_duration = pulse_end -pulse_start
            # Part 7:Multiply with (by?) the sonic speed (34300 cm/s)
            #divied by 2 because there and back
            distance = (pulse_duration * 34300) / 2
            return distance
        
        except:
            GPIO.cleanup()
            distance = -1
            return distance
        


