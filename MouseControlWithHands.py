import time
import autopy
# import pyautogui
import cv2
import numpy as np
import HandTrackingModule as htm

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 50            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

radius=7
thickness=cv2.FILLED
pTime=0

obj=htm.HandTrack(maxHands=1,detectionCon=0.8)
screen_height,screen_width=autopy.screen.size()

VideoSource=cv2.VideoCapture(0)
VideoSource.set(3, width)           # Adjusting size
VideoSource.set(4, height)

while True:
    status,frame = VideoSource.read()
    frame=obj.processHands(frame)

    lmList=obj.findPosition(frame=frame,draw=False)
    
    if len(lmList)!=0:

        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)

        fingers=obj.fingersUp()

        cv2.rectangle(frame, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2) 
                
        if fingers[1]==1 and fingers[4]==1:
            distancebetween2fingers,frame,coordinates=obj.findDistance(frame,8,20,radius,thickness,True)
            print(distancebetween2fingers)

            if distancebetween2fingers>150 and distancebetween2fingers<300:
                frame=cv2.circle(center=(coordinates[4],coordinates[5]),color=(25, 227, 79),img=frame,radius=8,thickness=cv2.FILLED)
        
        if fingers[1]==1 and fingers[2]==1:
            distancebetween2fingers,frame,coordinates=obj.findDistance(frame,8,12,radius,thickness,True)
            print(distancebetween2fingers)

            if distancebetween2fingers<50:
                frame=cv2.circle(center=(coordinates[4],coordinates[5]),color=(25, 227, 79),img=frame,radius=8,thickness=cv2.FILLED)
                autopy.mouse.click()
                # pyautogui.click()
                
        if fingers[1]==1 and fingers[2]==0:
            
            x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
            y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            # pyautogui.moveTo(screen_width - curr_x, curr_y)

            autopy.mouse.smooth_move(screen_width - curr_x, curr_y)    # Moving the cursor
            cv2.circle(frame, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

    currentTime=time.time()
    fps=1//(currentTime-pTime)
    pTime=currentTime

    cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)
    cv2.imshow("Mouse Cotrol Panel: ",frame)
    cv2.waitKey(1)