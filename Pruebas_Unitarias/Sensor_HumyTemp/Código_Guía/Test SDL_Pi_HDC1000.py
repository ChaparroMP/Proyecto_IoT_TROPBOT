#!/usr/bin/env python
#
# Test SDL_Pi_HDC1000
#
# June 2017
#

#imports

import sys          
import time
import datetime
import SDL_Pi_HDC1000



# Main Program

print ("")
print ("Test SDL_Pi_HDC1000 Version 1.1 - SwitchDoc Labs")
print ("")
print ("Sample uses 0x40 and SwitchDoc HDC1000 Breakout board ")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("")

sen_hdc = SDL_Pi_HDC1000.SDL_Pi_HDC1000()

print ("------------")
print ("Manfacturer ID=0x%X"% sen_hdc.readManufacturerID()) 
print ("Device ID=0x%X"% sen_hdc.readDeviceID()) 
print ("Serial Number ID=0x%X"% sen_hdc.readSerialNumber())  
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())
# turn heater on
print ("turning Heater On")
sen_hdc.turnHeaterOn() 
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())
# turn heater off
print ("turning Heater Off")
sen_hdc.turnHeaterOff() 
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())

# change temperature resolution
print ("change temperature resolution")
sen_hdc.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())
# change temperature resolution
print ("change temperature resolution")
sen_hdc.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())

# change humdity resolution
print ("change humidity resolution")
sen_hdc.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_8BIT)
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())
# change humdity resolution
print ("change humidity resolution")
sen_hdc.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % sen_hdc.readConfigRegister())

while True:
        
        print ("-----------------")
        print ("Temperature = %3.1f C" % sen_hdc.readTemperature())
        print ("Humidity = %3.1f %%" % sen_hdc.readHumidity())
        time.sleep(3)
        print ("-----------------")

        