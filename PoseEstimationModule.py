import cv2
import time
import mediapipe as mpipe

def main():

    cap = cv2.VideoCapture(0)

    mpDraw=mpipe.solutions.drawing_utils
    mPose=mpipe.solutions.pose
    pose=mPose.Pose()

    while True:

        status,frame = cap.read()

        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame,results.pose_landmarks,mPose.POSE_CONNECTIONS)#,color=(0,0,255))

            for id,lm in enumerate(results.pose_landmarks.landmark):
                h,w,c=frame.shape

                cx,cy=lm.x*h,lm.y*w

                center=(int(cx),int(cy))

                cv2.circle(frame,center,5,(0,100,255),1)


        cv2.imshow("Pose",frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # cv2.waitKey(10)


if __name__=="__main__":
    main()
