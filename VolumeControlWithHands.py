import time
import math
import cv2
import numpy as np
import HandTrackingModule as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()


interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
interface=devices
volume.GetMute()
volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())
min_volume,max_volume= volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)

thickness=cv2.FILLED
radius=12

obj=htm.HandTrack(detectionCon=0.8)

VideoSource=cv2.VideoCapture(0)
pTime=0

while True:
    status,frame = VideoSource.read()
    # imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame=obj.processHands(frame)

    lmList=obj.findPosition(frame=frame,draw=False)

    
    if len(lmList)!=0:
        length, img, lineInfo = obj.findDistance(frame,4,8,radius,thickness,True)

        if length<50:
            frame=cv2.circle(center=(lineInfo[4],lineInfo[5]),color=(0,255,0),img=frame,radius=radius,thickness=thickness)
        elif length>300:
            frame=cv2.circle(center=(lineInfo[4],lineInfo[5]),color=(147, 227, 27),img=frame,radius=radius,thickness=thickness)
        else:
            range=np.interp(length,[50,300],[min_volume,max_volume])
            volBar=np.interp(length,[50,300],[350,50])
            volPercent=np.interp(length,[50,300],[0,100])

            print(int(length),range)    
            volume.SetMasterVolume(range,None)

            frame=cv2.rectangle(frame,(100,50),(140,350),(0,255,0),3)
            frame=cv2.rectangle(frame,(100,int(volBar)),(140,350),(0,255,0),cv2.FILLED)
            frame=cv2.putText(frame,str(volPercent),(100,470),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

    currentTime=time.time()
    fps=1//(currentTime-pTime)
    pTime=currentTime

    cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)
    cv2.imshow("Volumn Cotrol Panel: ",frame)
    cv2.waitKey(1)