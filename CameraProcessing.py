import cv2
import mediapipe as mpipe
import time
# import sys

# VIDEO_URL = str(sys.argv[1])

cap = cv2.VideoCapture(0)

mHands=mpipe.solutions.hands
hands=mHands.Hands()
mpDraw=mpipe.solutions.drawing_utils

currentTime=0
pTime=0
fps=0

while(True):
    ret, frame = cap.read()

    imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            for id,lm in enumerate(i.landmark):
                # print(id,lm)
                h,w,c=frame.shape
                cx,cy=(lm.x*w),(lm.y*h)
                if id==0 and id==4:
                    cv2.circle(frame,(cx,cy),20,(255,0,125),cv2.FILLED)
            mpDraw.draw_landmarks(frame,i,mHands.HAND_CONNECTIONS)


    currentTime=time.time()
    fps=1//(currentTime-pTime)
    pTime=currentTime

    cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

    cv2.imshow('Frame',frame)
    cv2.waitKey(1)