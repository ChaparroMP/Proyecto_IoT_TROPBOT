from __future__ import print_function
import paho.mqtt.publish as publish
#from bpm180 import bmp180
from time import sleep
import smbus
import sys

chanelLID = "" # enter chanel ID

apiKey = "" # enter apiKey

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
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTO} #FALTA
    tPort = 443
    tTLS = None
    
topic = "channels/"+channelID+"/publish/"+apiKey

sensor = 

temp = ""
humedad = ""

while(True)
    temp = 
    humedad = 
    
    print ("Temperatura =", temp, "   Humedad=", humedad)
    tPayload = "field1="+str(temp)+ "&field2=" + str(humedad)
    
    try:
        publish.single(topic, payload = tPayload, hostname=mqttHost, port=tPort, tls=) #FALTA
    except (KeyboardInterrupt)
        break
    except 
        print("There was an error while publishing the data")