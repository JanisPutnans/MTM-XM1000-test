import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import serial
import time
import matplotlib.dates as mdates
import datetime as dt
import matplotlib
matplotlib.rc('figure', figsize=(15, 10))



#from matplotlib import style
#import numpy as np
#import random


#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' 
ser.baudrate = 38400
ser.timeout = 10
ser.open()


D1 = -39.6
D2 = 0.01
C1 = -2.0468
C2 = 0.0367
C3 = -1.5955E-6
T1= 0.01
T2= 0.00008

arr_temp = []
arr_humidity = []
arr_light = []
xs = []

# #initialization function: plot the background of each frame
# def init():
#     fig = plt.figure()
#     ax1 = fig.add_subplot(3, 1, 1)
#     ax2 = fig.add_subplot(3, 1, 2)
#     ax3 = fig.add_subplot(3, 1, 3)
#    return fig,ax1,ax2,ax3



fig = plt.figure()
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)
main_title = fig.suptitle('Temperature, Humudity, Light')     
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.1)

def animate(i):
    try:
        ser_bytes = ser.readline() 
        temp, hum, light, *_ = list(map(str, ser_bytes.decode("utf-8").split(" ")))

        data_temp = float(temp)
        temperatureC =(data_temp*D2)+D1

        data_humidity= float(hum)
        humidity_Linear= C1+C2 * data_humidity +C3 *(data_humidity*data_humidity)
        RHtrue = (temperatureC - 25.0)*(T1+T2 * data_humidity) + humidity_Linear



        data_light = float(light)
        light_lux=2.5*((data_light)/4096)*6250


        arr_temp.append(temperatureC)
        arr_humidity.append(RHtrue)       
        arr_light.append(light_lux)
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    


        size = len(xs)
        if size >=50:
             arr_temp.pop(0)
             arr_humidity.pop(0)
             arr_light.pop(0)
             xs.pop(0)
    

        print(arr_temp)
        print(arr_humidity)
        print(arr_light)

        
        # clear axis
        ax1.cla()
        ax2.cla()
        ax3.cla()
 
        # Draw x and y lists
        ax1.plot(xs, arr_temp,label="Temperature")
        ax2.plot(xs, arr_humidity,label="Humidity")
        ax3.plot(xs, arr_light,label="Light")
        main_title.set_text('Temperature, Humudity, Light')
        return main_title,ax1,ax2,ax3


 

    except Exception as err:
        print("Communication read error ")  
        print(f"Unexpected {err=}, {type(err)=}")


anim = animation.FuncAnimation(fig, animate, interval=100, blit=False)
plt.show()