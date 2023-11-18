import cv2
import time
# import sys

# VIDEO_URL = str(sys.argv[1])

cap = cv2.VideoCapture(0)

currentTime=0
pTime=0
fps=0

while(True):
    ret, frame = cap.read()

    colorless=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blurred=cv2.medianBlur(colorless,5)
    
    edges=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,9)

    colorFrame=cv2.bilateralFilter(frame,9,250,250)

    cartoon=cv2.bitwise_and(colorFrame,colorFrame,mask=edges)

    currentTime=time.time()
    fps=1//(currentTime-pTime)
    pTime=currentTime

    cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

    cv2.imshow('Frame',cartoon)
    cv2.waitKey(1)

