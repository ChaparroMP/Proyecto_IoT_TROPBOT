###############################################################################
#
# PRUEBA_UNION DE SENSORES Y GPS
#
# Agosto 26, 2021
#
###############################################################################


## --------------------- Inclusion of Standard Headers ----------------------##
import sys,time, serial
from datetime import datetime
## ------------------------ Inclusion of Own Headers ------------------------##
import HDC1080_Lib
import LTR390_Lib
import GPSProx_Lib

# Main Program

state=0

sen_hdc1080 = HDC1080_Lib.Sensor_HDC1080
sen_ltr390  = LTR390_Lib.Sensor_LTR390
GPS_Proximidad = GPSProx_Lib.GPS_Prox 


#Set GPIO Pins
GPIO_TRIGGER_d = 16 # GPIO 23
GPIO_ECHO_d = 18 # GPIO 24


ser = serial.Serial("/dev/ttyAMA0",9600)

while True:
    print("Este es el estado",state)

    if(state==0):#Crear el archivo para guardar los datos
        archi1=open("Datos_Pru_U.txt","w")
        archi1.write("---------------------------------------------------------------------\n") 
        archi1.write("          PRUEBA DE UNIÓN DE LOS SENSORES Y GPS \n") 
        archi1.write("  El programa empezó  -> "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n")  
        archi1.write("---------------------------------------------------------------------\n\n") 
        archi1.close()

        state=1
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state==1):#Colocar los vectores en cero
        
        Temp_data=[]
        Hum_data=[]
        ALS_data=[]
        UV_data=[]
        Prox_1_data=0

        state=2
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    elif(state==2): #Tomar 30 datos continuos de los sensores(rad y TempHum)
        
        for i in range(30):
            Temp_data.append(sen_hdc1080.read_Temperature())
            Hum_data.append(sen_hdc1080.read_Humidity())
            ALS_data.append(sen_ltr390.read_ambient_light())
            UV_data.append(sen_ltr390.read_radiation_UV())
        state=3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    elif(state==3):#Tomar dato de proximidad

        Prox_1_data=(GPS_Proximidad.distance(GPIO_TRIGGER_d,GPIO_ECHO_d))   
        print("Listo dato de Proximidad",Prox_1_data)
        ready_GPS=0
        state=4
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   
    elif(state==4):#Adquirir dato de GPS
        received_data = ser.readline()
        GPS_data = str(received_data)
        ready_GPS=GPS_Proximidad.conetion_GPS(GPS_data)

        if(ready_GPS==0):
            GPS_data_divide=["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

            Data_W_Temp=0
            Data_W_Hum=0
            Data_W_ALS=0
            Data_W_UV=0
            Data_W_Prox1=0

            state=5

            
        else:
            if GPS_data[2:9] == "$GPRMC,":
                print(GPS_data)
                GPS_data_divide = GPS_Proximidad.sym_to_text(GPS_data)
                 
                Data_W_Temp=0
                Data_W_Hum=0
                Data_W_ALS=0
                Data_W_UV=0
                Data_W_Prox1=0

                state=5
            else:
                state=4
               
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    elif(state==5): #Calcular el promedio de los datos
        
        for i in range(30):
            Data_W_Temp +=Temp_data[i]
            Data_W_Hum +=Hum_data[i]
            Data_W_ALS +=ALS_data[i]
            Data_W_UV  +=UV_data[i]
        
        Data_W_Temp=round(Data_W_Temp/30,3)
        Data_W_Hum=round(Data_W_Hum/30,3)
        Data_W_ALS=round(Data_W_ALS/30,3)
        Data_W_UV=round(Data_W_UV/30,3)
        Data_W_Prox1=round(Prox_1_data,3)
    
        if(Data_W_Hum >= 85):
            sen_hdc1080.Turn_ON_Heater()
        else:
            sen_hdc1080.Turn_OFF_Heater()

        state=6

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    elif(state==6): #Imprimir datos en la terminal

        print("-----------------------------------------------------------------------------------")
        print("          Toma de datos --> "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n") 
        print("Fecha = " + GPS_data_divide[13]+ "/" + GPS_data_divide[14] + "/" + GPS_data_divide[15])
        print("Hora="+ GPS_data_divide[0] + ":" + GPS_data_divide[1]  + ":" + GPS_data_divide[2])
        print("Latitud = " + GPS_data_divide[3] + "° " + GPS_data_divide[4] + "'" + GPS_data_divide[5] + "." + GPS_data_divide[6] + GPS_data_divide[7])
        print("Longitud = " + GPS_data_divide[8] + "° " + GPS_data_divide[9] + "'" + GPS_data_divide[10] + "." + GPS_data_divide[11] + "," + GPS_data_divide[12]+"\n")
        
        print("Distancia                 = ", Data_W_Prox1, " [cm]")
        print("Temperatura Ambiente      = ", Data_W_Temp, " [ºC]")
        print("Humedad Relativa del aire = ", Data_W_Hum, " [%]")
        print("Luz Ambiente              = ", Data_W_ALS, " [lux]")
        print("Radiación UV              = ", Data_W_UV, " [nW/cm^2]")

        print("-----------------------------------------------------------------------------------") 

        state=7

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state==7): #Guardar datos adquiridos por sensores y GPS
        archi1=open("Datos_Pru_U.txt","a")
        archi1.write("          Toma de datos -->  "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
        archi1.write("GPS  "+ GPS_data +"\n") 
        archi1.write("Fecha = " + GPS_data_divide[13]+ "/" + GPS_data_divide[14] + "/" + GPS_data_divide[15]+"\n")
        archi1.write("Hora="+ GPS_data_divide[0] + ":" + GPS_data_divide[1]  + ":" + GPS_data_divide[2]+"\n")
        archi1.write("Latitud = " + GPS_data_divide[3] + "° " + GPS_data_divide[4] + "'" + GPS_data_divide[5] + "." + GPS_data_divide[6] + GPS_data_divide[7]+"     ")
        archi1.write("Longitud = " + GPS_data_divide[8] + "° " + GPS_data_divide[9] + "'" + GPS_data_divide[10] + "." + GPS_data_divide[11] + "," + GPS_data_divide[12]+"\n\n")
        
        archi1.write("Distancia                 = "+ str(Data_W_Prox1)+ " [cm]"+"\n")
        archi1.write("Temperatura Ambiente      = "+ str(Data_W_Temp)+ " [ºC]"+"\n")
        archi1.write("Humedad Relativa del aire = "+ str(Data_W_Hum)+ " [%]"+"\n")
        archi1.write("Luz Ambiente              = "+ str(Data_W_ALS)+ " [lux]"+"\n")
        archi1.write("Radiación UV              = "+ str(Data_W_UV)+ " [nW/cm^2]"+"\n")

        archi1.write("---------------------------------------------------------------------\n") 

        archi1.close()

        time_initial=datetime.now()

        state=8

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state==8):#Verificar la humedad para activar el HEATER y esperar 0 minutos para próxima medida
        rev_Hum=sen_hdc1080.read_Humidity()
        if(rev_Hum >= 85):
            sen_hdc1080.Turn_ON_Heater()
        else:
            sen_hdc1080.Turn_OFF_Heater()

#         time_final=datetime.now()
#         tiempo=time_final-time_initial
#         segundos=tiempo.seconds
# 
#         if(segundos==60):
#             state=1
        state=1
 
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
    else:
        state=state
