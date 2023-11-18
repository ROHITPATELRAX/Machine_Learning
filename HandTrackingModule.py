import cv2 
import time
import mediapipe as mpipe
import math

class HandTrack():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.tipIds = [4, 8, 12, 16, 20]

        self.mHands=mpipe.solutions.hands
        self.hands=self.mHands.Hands()
        self.mpDraw=mpipe.solutions.drawing_utils
    
    def processHands(self,frame,draw=True):
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame,i,self.mHands.HAND_CONNECTIONS)
        return frame
    
    def findPosition(self,frame,handNo=0,draw=True):
        self.lmList=list()
        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(hands.landmark):
                h,w,c=frame.shape
                cx,cy=(lm.x*w),(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    # if id==4 or id==8 :
                        cv2.circle(center=(int(cx),int(cy)),color=(0,0,225),img=frame,radius=20)
                        # cv2.circle(frame,(cx,cy),20,(0,0,225),cv2.FILLED)
        return self.lmList
    
    def fingersUp(self):
        fingers=[]
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def findDistance(self,frame,point1,point2,radius,thickness,draw=True,color=(255,0,25)):
        x1,y1=int(self.lmList[point1][1]),int(self.lmList[point1][2])
        x2,y2=int(self.lmList[point2][1]),int(self.lmList[point2][2])
        cx,cy=int((x2+x1)//2),int((y2+y1)//2)
        if draw:
            frame=cv2.circle(center=(int(x1),int(y1)),color=color,img=frame,radius=radius,thickness=thickness)
            frame=cv2.circle(center=(int(x2),int(y2)),color=color,img=frame,radius=radius,thickness=thickness)
            frame=cv2.line(color=color,img=frame,pt1=(x1,y1),pt2=(x2,y2),thickness=3)
            frame=cv2.circle(center=(cx,cy),color=color,img=frame,radius=radius,thickness=thickness)
        
        length=math.hypot(x2-x1,y2-y1)

        return length,frame,[x1,y1,x2,y2,cx,cy]
    

def main():

    cap=cv2.VideoCapture(0)

    currentTime=0
    pTime=0
    fps=0

    handTracker=HandTrack()

    while(True):
        status, frame = cap.read()

        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        frame=handTracker.processHands(frame,imgRGB)

        lmList=handTracker.findPosition(frame,draw=True)

        # print(lmList)

        currentTime=time.time()
        fps=1//(currentTime-pTime)
        pTime=currentTime

        cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

        cv2.imshow('Frame',frame)

        cv2.waitKey(1)

if __name__=="__main__":
    main()