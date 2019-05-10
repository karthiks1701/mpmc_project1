import cv2

import time
import serial #Serial imported for Serial communication


import numpy as np

ArduinoSerial = serial.Serial('com12',9600) 
time.sleep(2) 


cap=cv2.VideoCapture(0)
prevy=0
prevx=0


while(1):
    t0=time.time()
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_red = np.array([98,109,20]) 
    upper_red = np.array([112,255,255])

    mask = cv2.inRange(hsv,lower_red,upper_red)

    kernelOpen=np.ones((2,2))
    kernelClose=np.ones((20,20))

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    cnts,hierarchy=cv2.findContours(maskFinal,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max=0
    d=[]
    for c in cnts:
      if cv2.contourArea(c)>max:
           max=cv2.contourArea(c)
           d=c
    M = cv2.moments(d)
    cX = int(M["m10"]/M["m00"])
    cY = int(M["m01"]/M["m00"])
    
    
    res = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',maskClose)
    cv2.imshow('res',res)

    k=cv2.waitKey(1)&0xFF
    
    if k==27:
        cv2.destroyAllWindows()
        break
    t1=time.time()
    if ((prevy-cY)/(t1-t0+0.00001)>1000):
        up=1
    if ((prevy-cY)/(t1-t0+0.00001)<-1000):
        up=-1
    if ((prevy-cY)/(t1-t0+0.00001)<1000 and(prevy-cY)/(t1-t0+0.00001)>-1000):
        up=0
    if ((prevx-cX)/(t1-t0+0.00001)>1000):
        left=1
    if ((prevx-cX)/(t1-t0+0.00001)<-1000):
        left=-1
    if (((prevx-cX)/(t1-t0+0.00001)<1000) and ((prevx-cX)/(t1-t0+0.00001)>-1000)):
        left=0
    #print(left)
    #print(up)
    prevy=cY
    prevx=cX       
     
    if (left== 1): #if the value is 1
        ArduinoSerial.write(b'2') #send 1
    
    #if (left=='0') and (up=='0'): #if the value is 0
        #ArduinoSerial.write(b'0') #send 0
    
    if (left== -1): #if the value is 1
        ArduinoSerial.write(b'3') #send 1
    if (up==1): #if the value is 0
         
         ArduinoSerial.write(b'1') #send 0
        
    if(up==-1):
         ArduinoSerial.write(b'0')
