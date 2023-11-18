import numpy as np
import cv2


class BouncyBall:
    def __init__(self,height,width,frameName="Bouncy Ball",radius=30,maxSpeed=21,minSpeed=1,defaultSpeed=10) -> None:
        self.height=height
        self.width=width
        self.FrameName=frameName
        self.radius=radius
        self.maxSpeed=maxSpeed
        self.minSpeed=minSpeed
        self.defaultSpeed=defaultSpeed

    def MoveBall(self):
        cv2.namedWindow(self.FrameName)

        speed=self.defaultSpeed

        ballMovePointer=self.radius
        vertical=False

        upDownFlag=False

        while True:
            if ((ballMovePointer+speed+self.radius)>=self.width):
                upDownFlag=True
            
            elif ((ballMovePointer+speed-self.radius)<=0):
                upDownFlag=False
            
            img=np.zeros((self.height,self.width,3),np.uint8)

            cv2.putText(img=img,color=(230,230,0),text=f"Speed: {speed}",fontFace=cv2.FONT_HERSHEY_COMPLEX,org=(335,500),fontScale=1,thickness=3)
            if vertical:
                cv2.circle(img,(int(self.height/2),ballMovePointer),self.radius,(253,0,255),cv2.FILLED)
            else:
                cv2.circle(img,(ballMovePointer,int(self.width/2)),self.radius,(150,0,255),cv2.FILLED)
            
            cv2.imshow(self.FrameName,img)

            if upDownFlag:
                ballMovePointer-=speed
            else:
                ballMovePointer+=speed

            inpFromKeyboard=cv2.waitKey(27) & 0xff

            if inpFromKeyboard==82:
                speed+=1
            
            if inpFromKeyboard==ord('v'):
                vertical= not vertical

            if speed==self.maxSpeed:
                speed=self.minSpeed

            if inpFromKeyboard==ord('q'):
                break

        cv2.destroyAllWindows()

    def MoveBallInAllDirWithoutKey(self):
        
        x_blocker=False
        y_blocker=False

        x_mover=False
        y_mover=False

        x=int(self.height/2)+self.radius
        y=int(self.width/2)

        dx=1
        dy=1

        speed=self.defaultSpeed

        while True:
            img=np.zeros((self.height,self.width,3),dtype=np.uint8)
            cv2.putText(color=(255,250,0),img=img,org=(340,500),text=f"Speed: {speed}",fontFace=cv2.FONT_HERSHEY_COMPLEX,thickness=3,fontScale=1)
            
            if not x_blocker:
                x=x+dx
            if not y_blocker:
                y=y+dy
            
            if y+self.radius>=self.width or y-self.radius<=0:
                dy*=-1
            if x+self.radius>=self.height or x-self.radius<=0:
                dx*=-1
            
            cv2.circle(center=(x,y),color=(25,0,255),img=img,radius=self.radius,thickness=cv2.FILLED)

            cv2.imshow(self.FrameName,img)
            
            inpFromKeyboard=cv2.waitKey(27) & 0xff
            if inpFromKeyboard==82:
                speed+=1
                if speed==self.maxSpeed:
                    speed=self.minSpeed
            if inpFromKeyboard==84:
                pass
                            
            if inpFromKeyboard==81:
                x_blocker=not x_blocker
            if inpFromKeyboard==83:
                y_blocker=not y_blocker

            if inpFromKeyboard==ord('q'):
                break

    def MoveBallInAllDirWithKey(self):
        
        x=int(self.height/2)+self.radius
        y=int(self.width/2)

        dx=1
        dy=1

        speed=self.defaultSpeed

        while True:
            img=np.zeros((self.height,self.width,3),dtype=np.uint8)
            cv2.putText(color=(255,250,0),img=img,org=(340,500),text=f"Speed: {speed}",fontFace=cv2.FONT_HERSHEY_COMPLEX,thickness=3,fontScale=1)
            
            x+=dx
            y+=dy

            cv2.circle(center=(x,y),color=(25,0,255),img=img,radius=self.radius,thickness=cv2.FILLED)

            cv2.imshow(self.FrameName,img)
            
            inpFromKeyboard=cv2.waitKey(27) & 0xff
                       
            if inpFromKeyboard==81:
                if x-self.radius>0 and dx!=-1:
                    dx*=-1
            if inpFromKeyboard==82:
                if x+self.radius<self.height and dx==1:
                    dx*=1
            if inpFromKeyboard==83:
                if y-self.radius>0 and dy!=-1:
                    dy*=-1
            if inpFromKeyboard==84:
                if y+self.radius<self.width and dy==1:
                    dy*=1
            
            if inpFromKeyboard==ord('p'):
                speed+=1
                if speed==self.maxSpeed:
                    speed=self.minSpeed
            if inpFromKeyboard==ord('q'):
                break

def main():
    height=512
    width=512

    obj=BouncyBall(height,width)
    obj.MoveBallInAllDirWithKey()

if __name__=="__main__":
    main()
