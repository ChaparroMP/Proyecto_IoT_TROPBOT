###############################################################################
#
# VERSIÓN 1 - FSM de TROPBOT
#
# Noviembre 21 2021
#
# Diseñado por: Castillo Lorena, Chaparro Pilar & Varón Jelitza
#
###############################################################################

## ------------------- Inclusión de liberías estándar -----------------------##
from __future__ import print_function
import paho.mqtt.publish as publish
import sys, time, serial, csv, os, smbus
import ADS1015V3
import RPi.GPIO as GPIO
import dropbox,requests


## ------------------ Inclusión de librerías propias ------------------------##
import HDC1080_Lib
import LTR390_Lib
import GPSProx_Lib
import mq135_Lib
## -------------- Declaraciones para canal Thingspeak -----------------------##

# Canal 1
channelID_1 = "1579111"  #Enter your Channel ID here
apiKey_1 = "051FJUNTN545MJ7L"  #Enter your WriteAPI key here

# Canal 2
channelID_2 = "1579112"  #Enter your Channel ID here
apiKey_2 = "ZAXLGJ9J09APJX93"  #Enter your WriteAPI key here

useUnsecuredTCP = False
useUnsecuredWebsockets = False
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"


if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
topic_1 = "channels/" + channelID_1 + "/publish/" + apiKey_1
topic_2 = "channels/" + channelID_2 + "/publish/" + apiKey_2



## ------------------ Función de Conexión a Internet-------------------------##
def check_connection(url = 'https://www.google.com/'):
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Conectado a Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No se ha establecido Conexión a Internet.")
        return False


## ---------------------- Declaración de variables----------------------------##
sen_hdc1080 = HDC1080_Lib.Sensor_HDC1080
sen_ltr390  = LTR390_Lib.Sensor_LTR390
GPS_Proximidad = GPSProx_Lib.GPS_Prox 

#Definir puertos GPIO
TRIGGER_prox1 = 18 
ECHO_prox1 = 16 

TRIGGER_prox2 = 22 
ECHO_prox2 = 24

TRIGGER_prox3 = 11 
ECHO_prox3 = 13 

TRIGGER_prox4 = 29 
ECHO_prox4 = 31 

BTN_inicio_VEX_RPI =7
BTN_medir_VEX_RPI =12
BTN_fin_VEX_RPI =15

LED_internet =26
LED_enviar =19

SIG_enable_RPI_VEX = 21
SIG_finMedida_RPI_VEX = 23
SIG_conexionInternet_RPI_VEX = 40
SIG_prox1_RPI_VEX = 35
SIG_prox2_RPI_VEX = 32 
SIG_prox3_RPI_VEX = 36
SIG_prox4_RPI_VEX = 38



#Config. GPIO  (IN/OUT)
GPIO.setup(TRIGGER_prox1, GPIO.OUT)
GPIO.setup(TRIGGER_prox2, GPIO.OUT)
GPIO.setup(TRIGGER_prox3, GPIO.OUT)
GPIO.setup(TRIGGER_prox4, GPIO.OUT)

GPIO.setup(ECHO_prox1, GPIO.IN)
GPIO.setup(ECHO_prox2, GPIO.IN)
GPIO.setup(ECHO_prox3, GPIO.IN)
GPIO.setup(ECHO_prox4, GPIO.IN)

GPIO.setup(LED_internet, GPIO.OUT)
GPIO.setup(LED_enviar, GPIO.OUT)

GPIO.setup(SIG_enable_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_finMedida_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_conexionInternet_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_prox1_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_prox2_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_prox3_RPI_VEX, GPIO.OUT)
GPIO.setup(SIG_prox4_RPI_VEX, GPIO.OUT)


GPIO.setup(BTN_inicio_VEX_RPI, GPIO.IN)
GPIO.setup(BTN_medir_VEX_RPI, GPIO.IN)
GPIO.setup(BTN_fin_VEX_RPI, GPIO.IN)


#Configurar UART para GPS
ser = serial.Serial("/dev/ttyAMA0",9600)


# Config iniciales para CO2
Channel = 3
PGA=6144
DataRate=250


#Para Dropbox
dbx = dropbox.Dropbox('MGP3Pacj7vUAAAAAAAAAAXebVRxpkSCvPbdy_hnsyW1sm4jwhb8fkMKLIdWkmxOG')

## -----------------------------Main Program----------------------------------##
num_med=0
adquirir_completo=0

state_general=0
state_adq=0


while True:
    print("Este es el estado FSM PRINCIPAL",state_general)
    print("Este es el estado FSM ADQUISION",state_adq)
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    if(state_general==0): # Inicializar variables

        state_adq=0
        num_med=0
        GPIO.output(LED_internet, False)
        GPIO.output(LED_enviar, False)
        
        #Lógica negada para CORTEX
        GPIO.output(SIG_enable_RPI_VEX, True)
        GPIO.output(SIG_finMedida_RPI_VEX, True)
        GPIO.output(SIG_conexionInternet_RPI_VEX, True)
        GPIO.output(SIG_prox1_RPI_VEX, True)
        GPIO.output(SIG_prox2_RPI_VEX,True)
        GPIO.output(SIG_prox3_RPI_VEX, True)
        GPIO.output(SIG_prox4_RPI_VEX, True)
        

        state_general=1

 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    elif(state_general==1): # Esperar BTN_inicio_VEX_RPI (desde cortex)

        if(GPIO.input(BTN_inicio_VEX_RPI) == 1):
            archi1= open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG_TEMP.csv', "w", newline='')
            spamreader = csv.writer(archi1)
            spamreader.writerow(["FECHA","HORA","DATA_TEMPERATURA[°C]","DATA_HUMEDAD[%]",
            "DATA_LUZ_AMBIENTE[Lux]","DATA_UV[nW/cm^2]","DATA_CO2[ppm]" ,"DATA_PROX_ADELANTE[cm]",
            "DATA_PROX_DERECHA[cm]", "DATA_PROX_IZQUIERDA[cm]", "DATA_PROX_ATRAS[cm]",
            "LATITUD", "LONGITUD"])
            archi1.close()
            
            archi2= open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT_TEMP.csv', "w", newline='')
            spamreader = csv.writer(archi2)
            spamreader.writerow(["FECHA","HORA","DATA_TEMPERATURA[°C]","DATA_HUMEDAD[%]",
            "DATA_LUZ_AMBIENTE[Lux]","DATA_UV[nW/cm^2]" ,"DATA_PROX_ADELANTE[cm]",
            "LATITUD", "LONGITUD"])
            archi2.close()

            archi3= open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_TG.csv', "w", newline='')
            spamreader = csv.writer(archi3)
            spamreader.writerow(["FECHA","HORA","DATA_TEMPERATURA[°C]","DATA_HUMEDAD[%]",
            "DATA_LUZ_AMBIENTE[Lux]","DATA_UV[nW/cm^2]","DATA_CO2[ppm]" ,"DATA_PROX_ADELANTE[cm]",
            "DATA_PROX_DERECHA[cm]", "DATA_PROX_IZQUIERDA[cm]", "DATA_PROX_ATRAS[cm]",
            "LATITUD", "LONGITUD"])
            archi3.close()

            archi4= open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_IoT.csv', "w", newline='')
            spamreader = csv.writer(archi4)
            spamreader.writerow(["FECHA","HORA","DATA_TEMPERATURA[°C]","DATA_HUMEDAD[%]",
            "DATA_LUZ_AMBIENTE[Lux]","DATA_UV[nW/cm^2]" ,"DATA_PROX_ADELANTE[cm]",
            "LATITUD", "LONGITUD"])
            archi4.close()

            state_general = 2
        else:
            state_general = 1
 
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state_general==2): # Verificar sensores de prox y esperar
                            # Botón medida
        
        dist1=0
        dist2=0
        dist3=0
        dist4=0

        Prox1_data=[]
        Prox2_data=[]
        Prox3_data=[]
        Prox4_data=[]
        
        state_adq=0
        adquirir_completo=0

        for i in range(10):
            Prox1_data.append(GPS_Proximidad.distance(TRIGGER_prox1,ECHO_prox1))
            Prox2_data.append(GPS_Proximidad.distance(TRIGGER_prox2,ECHO_prox2))
            Prox3_data.append(GPS_Proximidad.distance(TRIGGER_prox3,ECHO_prox3))
            Prox4_data.append(GPS_Proximidad.distance(TRIGGER_prox4,ECHO_prox4))

         
        for i in range(10):
            dist1 += Prox1_data[i]
            dist2 += Prox2_data[i]
            dist3 += Prox3_data[i]
            dist4 += Prox4_data[i]


        dist1= round(dist1/10,3)
        dist2= round(dist2/10,3)
        dist3= round(dist3/10,3)
        dist4= round(dist4/10,3)

        if(dist1 < 21):
            GPIO.output(SIG_prox1_RPI_VEX, False)
            
        else:
            GPIO.output(SIG_prox1_RPI_VEX, True) 
        #--------------------------------------------
        if(dist2 < 21):
            GPIO.output(SIG_prox2_RPI_VEX, False)
            
        else:
            GPIO.output(SIG_prox2_RPI_VEX, True) 

        #--------------------------------------------
        if(dist3 < 21):
            GPIO.output(SIG_prox3_RPI_VEX, False)
            
        else:
            GPIO.output(SIG_prox3_RPI_VEX, True) 

        #--------------------------------------------
        if(dist4 < 21):
            GPIO.output(SIG_prox4_RPI_VEX, False)
            
        else:
            GPIO.output(SIG_prox4_RPI_VEX, True)


        #/////////////////////////////////////////////
        print("Botón medir", GPIO.input(BTN_medir_VEX_RPI))
        if(GPIO.input(BTN_medir_VEX_RPI) == 1):
            state_general = 3
        elif(GPIO.input(BTN_fin_VEX_RPI) == 1 and num_med > 0):
            state_general = 5
        else:
            state_general = 2


 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state_general==3): #ADQUISIÓN SENSORES
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
        while(adquirir_completo==0):
            if(state_adq==0):#Colocar los vectores en cero
                Temp_data=[]
                Hum_data=[]
                ALS_data=[]
                UV_data=[]
                CO2_data=[]
                Prox_1_data=[]
                Prox_2_data=[]
                Prox_3_data=[]
                Prox_4_data=[]
                
                state_adq =1
                state_general = 3
            
            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==1):#Tomar 30 datos continuos de los sensores
                for i in range(30):
                    Temp_data.append(sen_hdc1080.read_Temperature())
                    Hum_data.append(sen_hdc1080.read_Humidity())
                    ALS_data.append(sen_ltr390.read_ambient_light())
                    UV_data.append(sen_ltr390.read_radiation_UV())
                    
                    #------------Adquirir dato de CO2-------------------------------
                    AnalogIn = ADS1015V3.Read_ADC(Channel, PGA, DataRate)
                    mq135_sen = mq135_Lib.MQ135(AnalogIn)
                    CO2_data.append(mq135_sen.get_ppm(Temp_data[i], Hum_data[i]))
                    
                for i in range(11):
                    Prox_1_data.append(GPS_Proximidad.distance(TRIGGER_prox1,ECHO_prox1))
                    Prox_2_data.append(GPS_Proximidad.distance(TRIGGER_prox2,ECHO_prox2))
                    Prox_3_data.append(GPS_Proximidad.distance(TRIGGER_prox3,ECHO_prox3))
                    Prox_4_data.append(GPS_Proximidad.distance(TRIGGER_prox4,ECHO_prox4))
                    
                Data_W_Temp=0
                Data_W_Hum=0
                Data_W_ALS=0
                Data_W_UV=0
                Data_W_CO2=0
                Data_W_Prox1=0
                Data_W_Prox2=0
                Data_W_Prox3=0
                Data_W_Prox4=0
                ready_GPS=0

                state_adq =2
                state_general = 3

            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==2):#Adquirir dato de GPS
                received_data = ser.readline()
                GPS_data = str(received_data)
                ready_GPS=GPS_Proximidad.conection_GPS(GPS_data)

                if(ready_GPS==0):
                    GPS_data_divide=["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

                    Data_W_Temp=0
                    Data_W_Hum=0
                    Data_W_ALS=0
                    Data_W_UV=0
                    Data_W_CO2=0
                    Data_W_Prox1=0
                    Data_W_Prox2=0
                    Data_W_Prox3=0
                    Data_W_Prox4=0

                    state_adq = 3 
                    state_general = 3
            
                    
                else:
                    if (GPS_data[2:9] == "$GPRMC,"):
                        print(GPS_data)
                        GPS_data_divide = GPS_Proximidad.sym_to_text(GPS_data)
                        
                        Data_W_Temp=0
                        Data_W_Hum=0
                        Data_W_ALS=0
                        Data_W_UV=0
                        Data_W_CO2=0
                        Data_W_Prox1=0
                        Data_W_Prox2=0
                        Data_W_Prox3=0
                        Data_W_Prox4=0

                        state_adq = 3 
                        state_general = 3
                    else:
                        state_adq=2
                        state_general = 3

            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==3):#Ajustar el dato del GPS
                
                if(GPS_data_divide[7]=="S"):
                    Data_Latitud="-"+GPS_data_divide[3]+"."+GPS_data_divide[4]+GPS_data_divide[5]+GPS_data_divide[6]
                else:
                    Data_Latitud=GPS_data_divide[3]+"."+GPS_data_divide[4]+GPS_data_divide[5]+GPS_data_divide[6]
                    
                if(GPS_data_divide[12]=="W"):
                    Data_Longitud="-"+GPS_data_divide[8]+"."+GPS_data_divide[9]+GPS_data_divide[10]+GPS_data_divide[11]
                else:
                    Data_Longitud=GPS_data_divide[8]+"."+GPS_data_divide[9]+GPS_data_divide[10]+GPS_data_divide[11]

                Hora_actual=time.strftime("%X")
                Fecha_actual=time.strftime("%x")

                state_adq = 5
                state_general = 3
            
            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==5):#Calcular el promedio de los datos
                for i in range(30):
                    Data_W_Temp += Temp_data[i]
                    Data_W_Hum  += Hum_data[i]
                    Data_W_ALS  += ALS_data[i]
                    Data_W_UV   += UV_data[i]
                    Data_W_CO2  += CO2_data[i]
                
                for i in range(11):
                    Data_W_Prox1 += Prox_1_data[i]
                    Data_W_Prox2 += Prox_2_data[i]
                    Data_W_Prox3 += Prox_3_data[i]
                    Data_W_Prox4 += Prox_4_data[i]

        
                Data_W_Temp=round(Data_W_Temp/30,3)
                Data_W_Hum=round(Data_W_Hum/30,3)
                Data_W_ALS=round(Data_W_ALS/30,3)
                Data_W_UV=round(Data_W_UV/30,3)
                Data_W_CO2=round(Data_W_CO2/30,3)
                Data_W_Prox1=round(((Data_W_Prox1-Prox_1_data[0])/10),3)
                Data_W_Prox2=round(((Data_W_Prox2-Prox_2_data[0])/10),3)
                Data_W_Prox3=round(((Data_W_Prox3-Prox_3_data[0])/10),3)
                Data_W_Prox4=round(((Data_W_Prox4-Prox_4_data[0])/10),3)
            
                if(Data_W_Hum >= 80):
                    sen_hdc1080.Turn_ON_Heater()
                else:
                    sen_hdc1080.Turn_OFF_Heater()

                state_adq = 6
                state_general = 3

            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==6):#Imprimir datos en la terminal
                print("-----------------------------------------------------------------------------------")
                print("          Toma de datos --> "+ time.strftime("%Y-%m-%d %H:%M:%S")+"\n") 
                print("Fecha = " + GPS_data_divide[13]+ "/" + GPS_data_divide[14] + "/" + GPS_data_divide[15])
                print("Hora="+ GPS_data_divide[0] + ":" + GPS_data_divide[1]  + ":" + GPS_data_divide[2])
                print("Latitud = " + GPS_data_divide[3] + "° " + GPS_data_divide[4] + "'" + GPS_data_divide[5] + "." + GPS_data_divide[6] + GPS_data_divide[7])
                print("Longitud = " + GPS_data_divide[8] + "° " + GPS_data_divide[9] + "'" + GPS_data_divide[10] + "." + GPS_data_divide[11] + "," + GPS_data_divide[12]+"\n")
                
                print("\n")
                print("Latitud_ThingSpeak  "+Data_Latitud)
                print("Longitud_ThingSpeak   "+Data_Longitud)
                print("\n")
                
                print("Distancia_Prox1           = ", Data_W_Prox1, " [cm]")
                print("Distancia_Prox2           = ", Data_W_Prox2, " [cm]")
                print("Distancia_Prox3           = ", Data_W_Prox3, " [cm]")
                print("Distancia_Prox4           = ", Data_W_Prox4, " [cm]\n")
                print("Temperatura Ambiente      = ", Data_W_Temp, " [ºC]")
                print("Humedad Relativa del aire = ", Data_W_Hum, " [%]")
                print("Luz Ambiente              = ", Data_W_ALS, " [lux]")
                print("Radiación UV              = ", Data_W_UV, " [nW/cm^2]")
                print("Dióxido de Carbono        = ", Data_W_CO2, " [ppm]")

                print("-----------------------------------------------------------------------------------") 

                state_adq = 7
                state_general = 3

            #/////////////////////////////////////////////////////////////////////////
            elif(state_adq==7):#Guardar datos adquiridos por sensores y GPS
                with open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG_TEMP.csv', 'a', newline='') as f_object: 
                    spamreader = csv.writer(f_object)
                    spamreader.writerow([Fecha_actual,Hora_actual,Data_W_Temp,Data_W_Hum, Data_W_ALS, Data_W_UV, Data_W_CO2,
                    Data_W_Prox1,Data_W_Prox2,Data_W_Prox3,Data_W_Prox4,Data_Latitud, Data_Longitud])
                    f_object.close()

                with open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT_TEMP.csv', 'a', newline='') as f_object_1: 
                    spamreader = csv.writer(f_object_1)
                    spamreader.writerow([Fecha_actual,Hora_actual,Data_W_Temp,Data_W_Hum, Data_W_ALS, Data_W_UV,
                    Data_W_Prox1,Data_Latitud, Data_Longitud])
                    f_object_1.close()
                
                with open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_TG.csv', 'a', newline='') as f_object_2: 
                    spamreader = csv.writer(f_object_2)
                    spamreader.writerow([Fecha_actual,Hora_actual,Data_W_Temp,Data_W_Hum, Data_W_ALS, Data_W_UV, Data_W_CO2,
                    Data_W_Prox1,Data_W_Prox2,Data_W_Prox3,Data_W_Prox4,Data_Latitud, Data_Longitud])
                    f_object_2.close()
                
                with open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_IoT.csv', 'a', newline='') as f_object_3: 
                    spamreader = csv.writer(f_object_3)
                    spamreader.writerow([Fecha_actual,Hora_actual,Data_W_Temp,Data_W_Hum, Data_W_ALS, Data_W_UV,
                    Data_W_Prox1,Data_Latitud, Data_Longitud])
                    f_object_3.close()
                
                GPIO.output(SIG_finMedida_RPI_VEX, False)
                num_med+=1
                print("NÚMERO DE MEDIDA: ", num_med)
                adquirir_completo=1
                state_adq = 0
                state_general = 4

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif(state_general==4): # Verficar botón fin de recorrido del CORTEX

        GPIO.output(SIG_finMedida_RPI_VEX, True)

        if(GPIO.input(BTN_fin_VEX_RPI) == 1):
            state_adq = 0
            state_general = 5
        else:
            state_adq = 0
            state_general = 2

 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state_general==5): #Revisar conexión a INTERNET y Manejo de archivos HISTÓRICO
        if check_connection():
            GPIO.output(LED_internet, True) 
            GPIO.output(SIG_conexionInternet_RPI_VEX, False)
            #//////////////////////////////////////////////////////////////////////////////////////////////////
            # Descargar Historico a RPI
            
            print("Descargando información a DROPBOX")
            dbx.files_download_to_file("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG.csv",
                                        "/Datos_TG/Datos_Historico_TROPBOT.csv")
        
            dbx.files_download_to_file("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT.csv",
                                       "/Datos_IoT/Datos_Historico_TROPBOT.csv")
            print("Descarga exitosa")
            #Eliminar Historico en DBX
            dbx.files_delete("/Datos_IoT/Datos_Historico_TROPBOT.csv")
            dbx.files_delete("/Datos_TG/Datos_Historico_TROPBOT.csv")
            print("Archivos eliminados")

            #//////////////////////////////////////////////////////////////////////////////////////////////////               
            #Crear/sobreescribir Historico

            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG_TEMP.csv", newline='') as csvfile1:
                reader = csv.DictReader(csvfile1)
                for row in reader:
                    list_data_temp=[]
                    list_data_temp = [row['FECHA'], row['HORA'], row['DATA_TEMPERATURA[°C]'],row['DATA_HUMEDAD[%]'],
                                      row['DATA_LUZ_AMBIENTE[Lux]'],row['DATA_UV[nW/cm^2]'],row['DATA_CO2[ppm]'],
                                      row['DATA_PROX_ADELANTE[cm]'],row['DATA_PROX_DERECHA[cm]'],row['DATA_PROX_IZQUIERDA[cm]'],
                                      row['DATA_PROX_ATRAS[cm]'],row['LATITUD'],row['LONGITUD']]
                    
                    with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG.csv", 'a', newline='') as f_object: 
                        writer_object = csv.writer(f_object)
                        writer_object.writerow(list_data_temp)
                        f_object.close()
                csvfile1.close()  
    
            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT_TEMP.csv", newline='') as csvfile2:
                reader = csv.DictReader(csvfile2)
                for row in reader:
                    list_data_temp=[]  
                    list_data_temp = [row['FECHA'], row['HORA'], row['DATA_TEMPERATURA[°C]'],row['DATA_HUMEDAD[%]'],
                                      row['DATA_LUZ_AMBIENTE[Lux]'],row['DATA_UV[nW/cm^2]'],
                                      row['DATA_PROX_ADELANTE[cm]'],row['LATITUD'],row['LONGITUD']]
                    
                    with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT.csv", 'a', newline='') as f_object1: 
                        writer_object = csv.writer(f_object1)
                        writer_object.writerow(list_data_temp)
                        f_object1.close()
                csvfile2.close()    
            
            #//////////////////////////////////////////////////////////////////////////////////////////////////               
            #Subir a DBX
            print("Enviando información a DROPBOX 1 Hist")
            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG.csv", "rb") as f_file:
                dbx.files_upload(f_file.read(), "/Datos_TG/Datos_Historico_TROPBOT.csv", mute = True)
                f_file.close()
            print("Envio exitoso")

            print("Enviando información a DROPBOX 2 Hist")
            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT.csv", "rb") as f_file1:
                dbx.files_upload(f_file1.read(), "/Datos_IoT/Datos_Historico_TROPBOT.csv", mute = True)
                f_file1.close()
            print("Envio exitoso")

            #//////////////////////////////////////////////////////////////////////////////////////////////////               
            #Eliminar Historico en RPI
            os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG.csv")
            os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_TG_TEMP.csv")
            os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT.csv")
            os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Datos_Historico_IoT_TEMP.csv")
            print("Eliminados los históricos locales")
            
            state_general = 6

        else:
            GPIO.output(SIG_conexionInternet_RPI_VEX, True)
            GPIO.output(LED_internet, False)
            print("No internet")

            #//////////////////REVISAR PROXIMIDAD////////////////////////////////////
            dist1=0
            dist2=0
            dist3=0
            dist4=0

            Prox1_data=[]
            Prox2_data=[]
            Prox3_data=[]
            Prox4_data=[]
        
            for i in range(10):
                Prox1_data.append(GPS_Proximidad.distance(TRIGGER_prox1,ECHO_prox1))
                Prox2_data.append(GPS_Proximidad.distance(TRIGGER_prox2,ECHO_prox2))
                Prox3_data.append(GPS_Proximidad.distance(TRIGGER_prox3,ECHO_prox3))
                Prox4_data.append(GPS_Proximidad.distance(TRIGGER_prox4,ECHO_prox4))

         
            for i in range(10):
                dist1 += Prox1_data[i]
                dist2 += Prox2_data[i]
                dist3 += Prox3_data[i]
                dist4 += Prox4_data[i]

            dist1= round(dist1/10,3)
            dist2= round(dist2/10,3)
            dist3= round(dist3/10,3)
            dist4= round(dist4/10,3)

            if(dist1 < 21):
                GPIO.output(SIG_prox1_RPI_VEX, False)
                
            else:
                GPIO.output(SIG_prox1_RPI_VEX, True) 
            #--------------------------------------------
            if(dist2 < 21):
                GPIO.output(SIG_prox2_RPI_VEX, False)
                
            else:
                GPIO.output(SIG_prox2_RPI_VEX, True) 

            #--------------------------------------------
            if(dist3 < 21):
                GPIO.output(SIG_prox3_RPI_VEX, False)
                
            else:
                GPIO.output(SIG_prox3_RPI_VEX, True) 

            #--------------------------------------------
            if(dist4 < 21):
                GPIO.output(SIG_prox4_RPI_VEX, False)
                
            else:
                GPIO.output(SIG_prox3_RPI_VEX, True) 

            #--------------------------------------------  
            state_general = 5
        
 
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    elif(state_general==6): # Manejo de archivos ACTUAL
        if check_connection():
            GPIO.output(LED_internet, True)
            GPIO.output(SIG_conexionInternet_RPI_VEX, True) 
            #------------------------------------------------------------------
            # Eliminar Actual en DBX
            dbx.files_delete("/Datos_IoT/Datos_Actual_TROPBOT.csv")
            dbx.files_delete("/Datos_TG/Datos_Actual_TROPBOT.csv")
            print("Archivos actuales eliminados")

            #------------------------------------------------------------------
            # Subir Actual a DBX 
            print("Enviando información a DROPBOX 1 Actual")
            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_TG.csv", "rb") as f_file:
                dbx.files_upload(f_file.read(), "/Datos_TG/Datos_Actual_TROPBOT.csv", mute = True)
                f_file.close()
            print("Envio exitoso 1 ")

            print("Enviando información a DROPBOX 2 Actual")
            with open("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_IoT.csv", "rb") as f_file1:
                dbx.files_upload(f_file1.read(), "/Datos_IoT/Datos_Actual_TROPBOT.csv", mute = True)
                f_file1.close()
            print("Envio exitoso 2")
            
            GPIO.output(LED_enviar, True)
            state_general = 8

        else:
            GPIO.output(LED_internet, False)
            GPIO.output(LED_enviar, False)
            GPIO.output(SIG_conexionInternet_RPI_VEX, True) 
            print("No internet")
            state_general = 6    
  
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif(state_general==8):
        
        if check_connection():
            GPIO.output(LED_internet, True) 
            #------------------------------------------------------------------
            # Leer archivo actual en RPI y Enviar datos a Thingspeak
            with open('/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_TG.csv', newline='') as csvfile3:
                reader = csv.DictReader(csvfile3)
                for row in reader:
                    tPayload = "field1=" + row['DATA_TEMPERATURA[°C]'] +"&field2=" + row['DATA_HUMEDAD[%]'] + "&field3=" + row['DATA_LUZ_AMBIENTE[Lux]']+ "&field4=" + row['DATA_UV[nW/cm^2]']+"&field5=" + row['DATA_CO2[ppm]']+"&field6=" + row['LATITUD'] + "&field7=" + row['LONGITUD'] 
                    
                    tPayload_2 = "field1=" + row['DATA_PROX_ADELANTE[cm]'] +"&field2=" + row['DATA_PROX_DERECHA[cm]']+ "&field3=" + row['DATA_PROX_IZQUIERDA[cm]'] +"&field4=" + row['DATA_PROX_ATRAS[cm]']
                               
 
                    try:
                        publish.single(topic_1, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
                        time.sleep(10)
                        publish.single(topic_2, payload=tPayload_2, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
                        time.sleep(10)


                    except (KeyboardInterrupt):
                        break

                    except:
                        print ("There was an error while publishing the data.")
                        state_general = 8
                
                #  Eliminar Actual en RPI
                os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_TG.csv")
                os.remove("/home/pi/Desktop/Proyecto-Grado-/Pruebas_Union_de_Sensores/FSM_Versions/Version1/Datos/Adq_Actual_IoT.csv")
                print("Eliminados los archivos actuales locales")

                GPIO.output(SIG_enable_RPI_VEX, False)
                state_general = 0 
                csvfile3.close()
            

        else:
            GPIO.output(LED_internet, False)
            GPIO.output(SIG_enable_RPI_VEX, True)
            print("No internet")
            state_general = 8
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    else:
        state_general=state_general

 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  




 # # PLANTILLA PARA NUEVO ESTADO (no borrar todavia, porfavorcito :3)

#     elif(state_general==):
        
#         state_general =       