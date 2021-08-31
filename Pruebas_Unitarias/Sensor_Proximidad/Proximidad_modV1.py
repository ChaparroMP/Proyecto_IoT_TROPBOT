  #Libraries
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#GPIO Mode (BOARD/BCM)
GPIO.setmode(GPIO.BOARD) #(GPIO.BCM)

#Set GPIO Pins
GPIO_TRIGGER = 16 # GPIO 23
GPIO_ECHO = 18 # GPIO 2

#Set GPIO direction (IN/OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    #set trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    #set trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    # save of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with (by?) the sonic speed (34300 cm/s)
    #divied by 2 because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

#print ("DEBUG")

state=0

while True:
    
    if(state==0):
        archi1=open("Datos_Proximidad.txt","w")
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.write("                PRUEBA PARA EL SENSOR DE PROXIMIDAD                  \n") 
        archi1.write("  El programa empezó a las -> "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n")  
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.close()
        
        state=1
        
    elif(state==1):
        dist = round(distance(),3)
        archi1=open("Datos_Proximidad.txt","a")
        archi1.write("Measured Distance ="+ str(dist)+"cm\n")
        archi1.write("---------------------------------------------------------------------\n")
        archi1.close()
        print("Measured Distance ="+ str(dist)+"cm\n")
        time.sleep(1)
        
    else:
        state=state
