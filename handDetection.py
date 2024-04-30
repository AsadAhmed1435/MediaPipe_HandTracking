import mediapipe as mp
import cv2
import time



class hand_detection:
    def __init__(self,mode=False,maxHands=2,modelcomplexity=0,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelcomplexity=modelcomplexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mphands = mp.solutions.hands
        self.hands=self.mphands.Hands(self.mode, self.maxHands,self.modelcomplexity,self.detectionCon,self.trackCon)
        self.mp_draw= mp.solutions.drawing_utils
        
    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
            
        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
              if draw:
                  self.mp_draw.draw_landmarks(img,hand_landmarks,self.mphands.HAND_CONNECTIONS)
                
        return img
    def findlocation(self,img,draw=True,handindex=0):
        self.lstlm=[]
       
        if self.result.multi_hand_landmarks:
            myhands= self.result.multi_hand_landmarks[handindex]
            for id , lm in enumerate(myhands.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.lstlm.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)                   
        return self.lstlm
    def findOpenFingers(self):
        fingrlst=[4,8,12,16,20]
        openfingr=[0,0,0,0,0]
        for i in range(1,5):
                if  self.lstlm[fingrlst[i]][2] < self.lstlm[fingrlst[i]-2][2]:
                    openfingr[i]=1 
                if self.lstlm[4][1] > self.lstlm[3][1]:
                    openfingr[0]=1 
        return openfingr
                        
    
   

def main():
    cap = cv2.VideoCapture(0)
    ptime=0
    ctime=0
    detector=hand_detection()
    lst=[]
    while(True):
        ret, frame = cap.read()
        img = detector.findHands(frame)
        lst=detector.findlocation(img,draw=False)
        if len(lst)!=0:
            openfingrs = detector.findOpenFingers()
            print(openfingrs)
        if len(lst)!=0:
            pass
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        
        cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    

if __name__=="__main__":
    main()