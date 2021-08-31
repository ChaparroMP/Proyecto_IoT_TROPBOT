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
        Temp_data=[]
        Hum_data=[]
        state=1
        
    elif(state==1):#CRear el archivo para guardar los datos
        
        Temp_data=[]
        Hum_data=[]
        state=2
        
    elif(state==2): #Tomar 30 datos continuos de Temp y Humedad
       
        for i in range(30):
            Temp_data.append(sen_hdc.read_Temperature())
            Hum_data.append(sen_hdc.read_Humidity())

        Data_W_Temp=0
        Data_W_Hum=0

        state=3

    
    elif(state==3): #Calcular el promedio de los datos
        
        for i in range(30):
            Data_W_Temp +=Temp_data[i]
            Data_W_Hum +=Hum_data[i]
        
        Data_W_Temp=round(Data_W_Temp/30,3)
        Data_W_Hum=round(Data_W_Hum/30,3)
    
        if(Data_W_Hum >= 85):
            sen_hdc.Turn_ON_Heater()
        else:
            sen_hdc.Turn_OFF_Heater()

        state=4

    elif(state==4): #Guardar datos promedio en el archivo y esperar 2 minutos para próxima medida
        archi1=open("Datos_Protocolo.txt","a")
        archi1.write("| "+time.strftime("%Y-%m-%d  |   %H:%M:%S")+"    |     "+str(Data_W_Temp)+" ºC     |      "+str(Data_W_Hum)+"%    |\n") 
        archi1.write("---------------------------------------------------------------------\n") 
        
        time_initial=datetime.now()

        state=5

    elif(state==5):#Verificar la humedad para activar el HEATER y esperar 3 minutos para próxima medida
        rev_Hum=sen_hdc.read_Humidity()
        if(rev_Hum >= 85):
            sen_hdc.Turn_ON_Heater()
        else:
            sen_hdc.Turn_OFF_Heater()

        time_final=datetime.now()
        tiempo=time_final-time_initial
        segundos=tiempo.seconds

        if(segundos==5):
            state=1
            
    else:
        state=state
