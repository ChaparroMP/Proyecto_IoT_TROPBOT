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
##        ╚═════╝         Bogota, D.C., August  26th, 2021.                   */
##                                                                            */
##          Copyright (C) Departament de Electronics                          */
##                        School of Engineering                               */
##                        Pontificia Universidad Javeriana                    */
##                        Bogota - Colombia - South America                   */
##                                                                            */
##*****************************************************************************/

#HY-SF05 Code Reference :https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#HY-SF05 Datasheet:https://datasheetspdf.com/pdf-file/813041/ETC/HY-SRF05/1



#GPS  Ublox NEO-6M v2  Code Reference :https://lastminuteengineers.com/neo6m-gps-arduino-tutorial/
#                                      https://medium.com/@kekreaditya/interfacing-u-blox-neo-6m-gps-module-with-raspberry-pi-1df39f9f2eba
#GPS  Ublox NEO-6M v2  Datasheet:https://www.u-blox.com/sites/default/files/products/documents/NEO-6_DataSheet_(GPS.G6-HW-09005).pdf



# --------------------- Inclusion of Standard Headers ----------------------##
import time
from time import sleep
import RPi.GPIO as GPIO


GPIO.setwarnings(False)

#GPIO Mode (BOARD/BCM)
GPIO.setmode(GPIO.BOARD) #(GPIO.BCM)


class GPS_Prox:

    #Define public functions

##FN############################################################################
#
#   sym_to_text(self,data);
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

                        GPS_vect_data=[local_hour, minute, second, deg, minn,sec,mils,coord, grados, min_l,sec_l,mils_l,coord_l,
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
#           Part 4: Save StartTime
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

        #* Part 1: Set GPIO direction (IN/OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        
        #* Part 2: Set trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
        
        #* Part 3: Set trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        #* Part 4: Save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
            
        #* Part 5: Save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        
        #* Part 6: Time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        #* Part 7: Multiply by the sonic speed (34300 cm/s)
        #          divied by 2 because there and back
        distance = (TimeElapsed * 34300) / 2
        
        return distance

