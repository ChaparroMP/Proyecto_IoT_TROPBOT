###############################################################################
#
# PRUEBA_HDC1080_PROTOCOLO
#
# Agosto 04, 2021
#
###############################################################################


## --------------------- Inclusion of Standard Headers ----------------------##
import sys          
import time
import datetime
from datetime import datetime
## ------------------------ Inclusion of Own Headers ------------------------##
import HDC1080_Func

# Main Program

state=0
sen_hdc = HDC1080_Func.Sensor_HDC1080

while True:
    if(state==0):#CRear el archivo para guardar los datos
        archi1=open("Datos_Protocolo.txt","w")
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.write("          PRUEBA PARA EL SENSOR DE TEMPERATURA Y HUMEDAD\n") 
        archi1.write("  El programa empezó  -> "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n")  
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.write("|    FECHA    |     HORA      |    TEMPERATURA    |      HUMEDAD     |\n")
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.close()
        
        time_initial=datetime.now()
        
        state=1
        
    elif(state==1):
        time_final=datetime.now()
        tiempo=time_final-time_initial
        segundos=tiempo.seconds

        if(segundos==60):
            state=2
        
    elif(state==2):#Tomar DATOS de Temp y Humedad
        
        Temp_data=(sen_hdc.read_Temperature())
        Hum_data=(sen_hdc.read_Humidity())
            
        print("Temperatura:"+str(round(Temp_data,3))+"°C")
        print("Humedad:"+str(round(Hum_data,3))+"% \n")
        
        archi1=open("Datos_Protocolo.txt","a")
        archi1.write("| "+time.strftime("%Y-%m-%d  |   %H:%M:%S")+"    |     "+str(round(Temp_data,3))+" ºC     |      "+str(round(Hum_data,3))+"%    |\n") 
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.close()

        state=3
    
    elif(state==3): #Verificar la humedad para encender el HEATER
        
        if(Hum_data >= 85):
            sen_hdc.Turn_ON_Heater()
        else:
            sen_hdc.Turn_OFF_Heater()

        state=1
            
    else:
        state=state

        

