#!/usr/bin/python
import os
import time
from math import sin, exp

def color(inp):
    if inp > 255:
         return 255
    if inp < 0:
         return 0
    return int(inp)

def t2color(t):
    r = (t - 45) * 2.5;
    g = 0;
    b = 420 - t * 2.6;
    return "%0.2X%0.2X%0.2X" % (color(r), color(g), color(b))    

def systemp():
    temps = os.popen("cat /sys/class/thermal/thermal_zone*/temp ").read()
    t = float(float(max(list(map(int, filter(len, temps.split("\n"))))))/ 1000.0)
    return t

dev = os.open("/dev/input/ckb1/cmd", os.O_RDWR)
os.write(dev, "active\n".encode())

t = systemp()
tcurr = t
tprev = t
tdelta = 3
i = 0
ratio = 0.98
iratio = 1 - ratio
phase = 0;
frame = 0.1
itemp = 5 / frame

while True:
    i = i + 1
    if i >= itemp:
        i = 0
        tcurr = systemp()
        """
        if (abs(tprev - tcurr) < tdelta ) and (abs(t - tcurr) < tdelta):
            #print("nothing to do")
            time.sleep(5)
            i = 100
        """

        tprev = tcurr        

    t = ratio * t + iratio * tcurr

    #t = 55

    mul =  max(1.3,  (t - 40) / 11.0);

    phase = phase + mul * frame; 
    
    x = phase;

    scale = pow(sin(x), 4)

    rgb1 = t2color(t)
    rgb2 = t2color(t + 30 * scale)
    rgb3 = t2color(t + 66 * scale)

    key = int(t / 10)

    #print( "t=%s color=%s" % (t, rgb1))
    cmd = "rgb %s g,y,u,i,l,o,m,n,b,7,8,f7,f8,space2:%s h,j,k:%s\n" % (rgb1, rgb2, rgb3)    
    #print(cmd)
    os.write(dev, cmd.encode())
    time.sleep(frame)
