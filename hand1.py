import cv2
import mediapipe as mp
import time
from keyPress import Button
from sound import note
import threading 

class handDetector():
    def __init__(self,  mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5, modelComplexity=1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplexity = modelComplexity
# 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw= mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNum = 0, draw = True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(myHand.landmark):

                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (0,0,255), cv2.FILLED)
        return lmList




def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        buttonList = [Button([0, 350], "C4"), Button([100, 350], "D4"), Button([200, 350], "E4"), Button([300, 350], "F4"), Button([400, 350], "G4"), Button([500, 350], "A4"), Button([600, 350], "B4")]
        i = 0
        for i in range(len((buttonList))):
             img = buttonList[i].keyCreate(img)
    
        if lmList:
             for button in buttonList:
                  x, y = button.pos
                  w, h = button.size

                  if ((x < lmList[4][1]<x+w and y < lmList[4][2]<y+h) or (x < lmList[8][1]<x+w and y < lmList[8][2]<y+h) or (x < lmList[12][1]<x+w and y < lmList[12][2]<y+h) or (x < lmList[16][1]<x+w and y < lmList[16][2]<y+h) or (x < lmList[20][1]<x+w and y < lmList[20][2]<y+h)):
                        cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x , y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
                        timer = threading.Thread(target = note, args = (button.text))
                        timer.start

                  

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 2, (255,155,240), 2)

        cv2.imshow("/Image", img)
        key = cv2.waitKey(1)
        if key == 27:
             break

if __name__ == "__main__":
    main()
