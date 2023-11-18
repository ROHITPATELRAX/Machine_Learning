import cv2
import mediapipe as mP
import sys

VIDEO_URL = str(sys.argv[1])

cap = cv2.VideoCapture(VIDEO_URL)

# retrieve FPS and calculate how long to wait between each frame to be display
# fps = cap.get(cv2.CAP_PROP_FPS)
# wait_ms = int(1000/fps)
# print('FPS:', fps)


count=0

while(True):
    # read one frame
    ret, frame = cap.read()

    print(frame)

    count+=1

    # display frame
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

print(count)