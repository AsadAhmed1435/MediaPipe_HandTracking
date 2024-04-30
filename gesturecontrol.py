import cv2
from handDetection import hand_detection
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#----------------------------------------****------------------------------------
cwidth,cheight=640,480
cap = cv2.VideoCapture(0)
cap.set(3,cwidth)
cap.set(4,cheight)
ptime=0
ctime=0
detector=hand_detection(maxHands=4)
lst=[]

#-----------------------------Volume---------------------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minvol = volRange[0]
maxvol=volRange[1]
volbar=400
volper=0


while(True):
    ret, frame = cap.read()
    img = detector.findHands(frame,draw=False)
    lst=detector.findlocation(img,draw=False)
    if len(lst)!=0:
        x1,y1=lst[4][1],lst[4][2]
        x2,y2=lst[8][1],lst[8][2]
        length = math.hypot(x2-x1,y2-y1)
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),5)
        
        
        vol = np.interp(length,[20,180],[minvol,maxvol])
        volbar = np.interp(length,[20,180],[400,150])
        volper = np.interp(length,[20,180],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        
    cv2.rectangle(img,(50,150),(85,400),(255,0,0))
    cv2.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(frame,f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),3)
        
        
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    cv2.putText(frame,f'{str(int(fps))}',(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()