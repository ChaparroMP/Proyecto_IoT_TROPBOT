import serial
from time import sleep

ser = serial.Serial("/dev/ttyAMA0")

def UTC_to_Local(hour):
    local_hour = int(hour) + 19 # diferencia horaria
    if local_hour > 24:
        local_hour -=  24
    local_hour = str(local_hour)
    return local_hour

def sym_to_text(data):
    if data[2:9] == "$GPRMC,":
        hour = data[9:11]
        minute = data[11:13]
        second = data[13:15]
        local_hour = UTC_to_Local(hour)
        print("Hora="+ local_hour + ":" + minute + ":" + second)
        row1=data[18:21]
        if row1 == ",A,":
            comma=data[21:].index(",")
            lat = data[21:22+(comma)]
            deg = lat[0:2]
            minn= lat[2:4]
            sec = lat[5:7]
            mils= lat[7:]
            coord = data[(21+comma+1)]
            print("Latitud = " + deg + "° " + minn + "'" + sec + "." + mils + coord)
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
                print("Longitud = " + grados + "° " + min_l + "'" + sec_l + "." + mils_l + "," + coord_l)
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
                    print("Fecha = " + dd + "/" + mm + "/" + yy)
while True:
    received_data = ser.readline()
    data = str(received_data)
    sym_to_text(data)
             
