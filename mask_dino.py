import cv2
from pynput.keyboard import Key,Controller



import numpy as np

keyboard = Controller()
cap=cv2.VideoCapture(0)
prev=0


while(1):
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_red = np.array([100,40,40])
    upper_red = np.array([105,255,255])

    mask = cv2.inRange(hsv,lower_red,upper_red)

    kernelOpen=np.ones((2,2))
    kernelClose=np.ones((20,20))

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    im2,cnts,hierarchy=cv2.findContours(maskFinal,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max=0
    d=[]
    for c in cnts:
      if cv2.contourArea(c)>max:
        max=cv2.contourArea(c)
        d=c
    M = cv2.moments(d)
    cX = int(M["m10"]/M["m00"])
    cY = int(M["m01"]/M["m00"])

    if prev-cY>5:
    
      keyboard.press(Key.up)

    print(str(cX)+","+str(cY))
    prev=cY

    res = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',maskClose)
    cv2.imshow('res',res)

    k=cv2.waitKey(1)&0xFF
    
    if k==27:
        cv2.destroyAllWindows()
        break


