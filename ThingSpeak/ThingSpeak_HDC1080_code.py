from __future__ import print_function
import paho.mqtt.publish as publish
import HDC1080_Lib
from time import sleep
import smbus
import sys


channelID = "1497497"  #Enter your Channel ID here

apiKey = "JZJQF8VET03WKQNX"  #Enter your WriteAPI key here


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
        
topic = "channels/" + channelID + "/publish/" + apiKey

sen_hdc1080 = HDC1080_Lib.Sensor_HDC1080

temp = ""
humidity = ""

while(True):
    
    temp = sen_hdc1080.read_Temperature()
    humidity = sen_hdc1080.read_Humidity()
    
    print (" Temperature =",temp ,"   Humidity =", humidity)

    tPayload = "field1=" + str(temp) + "&field2=" + str(humidity)

    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")

