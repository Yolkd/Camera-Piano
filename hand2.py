import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
from keyPress import Button
from keySound import note
import threading

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands = 2)

while True:
    
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    #hands = detector.findHands(img, draw=False)

    
    buttonList = [Button([0, 350], "C4"), Button([100, 350], "D4"), Button([200, 350], "E4"), Button([300, 350], "F4"), Button([400, 350], "G4"), Button([500, 350], "A4"), Button([600, 350], "B4")]
    for i in range(len((buttonList))):
             img = buttonList[i].keyCreate(img)


    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        hanType1 = hand1["type"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            timer = threading.Thread(target = note, args = (button.text))
            if ((x < lmList1[4][0]<x+w and y < lmList1[4][1]<y+h) or (x < lmList1[8][0]<x+w and y < lmList1[8][1]<y+h) 
                or (x < lmList1[12][0]<x+w and y < lmList1[12][1]<y+h) or (x < lmList1[16][0]<x+w and y < lmList1[16][1]<y+h) 
                or (x < lmList1[20][0]<x+w and y < lmList1[20][1]<y+h)):

                cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                timer.start

    if len(hands)==2:
        hand2 = hands[1]
        lmList2 = hand2["lmList"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            timer = threading.Thread(target = note, args = (button.text))
            if ((x < lmList2[4][0]<x+w and y < lmList2[4][1]<y+h) or (x < lmList2[8][0]<x+w and y < lmList2[8][1]<y+h) 
                or (x < lmList2[12][0]<x+w and y < lmList2[12][1]<y+h) or (x < lmList2[16][0]<x+w and y < lmList2[16][1]<y+h) 
                or (x < lmList2[20][0]<x+w and y < lmList2[20][1]<y+h)):

                cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                
                timer.start


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
         break

