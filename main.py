import cv2
from handDetection import hand_detection
import time

cap = cv2.VideoCapture(0)
ptime=0
ctime=0
detector=hand_detection(maxHands=4)
lst=[]
while(True):
    ret, frame = cap.read()
    img = detector.findHands(frame)
    lst=detector.findlocation(img,draw=False)
    if len(lst)!=0:
        print(lst[4])
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
