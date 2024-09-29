import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
from keyPress import Button
# from keySound import note
import threading
import pygame
import pygame.midi
import time

# from mido import Message, MidiFile, MidiTrack


pygame.init()
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

def conversion(note):
    convert = 12
    if (note[0] == 'C'):
        if (note[1] == "#"):
            convert*=int(note[2])+1
            convert+=1
        else:
            convert*=int(note[1])+1
    elif (note[0] == 'D'):
        if (note[1] == "#"):
            convert*=int(note[2])+1
            convert+=3
        else:
            convert*=int(note[1])+1
            convert+=2
    elif (note[0] == 'E'):
        convert*=int(note[1])+1
        convert+=4
    elif (note[0] == 'F'):
        if (note[1] == "#"):
            convert*=int(note[2])+1
            convert+=6
        else:
            convert*=int(note[1])+1
            convert+=5
    elif (note[0] == 'G'):
        if (note[1] == "#"):
            convert*=int(note[2])+1
            convert+=8
        else:
            convert*=int(note[1])+1
            convert+=7
    elif (note[0] == 'A'):
        if (note[1] == "#"):
            convert*=int(note[2])+1
            convert+=10
        else:
            convert*=int(note[1])+1
            convert+=9
    elif (note[0] == 'B'):
        convert*=int(note[1])+1
        convert+=11
    return convert

def merger(currentNotes, hand):
    if hand == 1:
        for i in range(len(currentNotes)):
            if not play_d[currentNotes[i]]:
                player.note_on(conversion(currentNotes[i]), 127)
                play_d[currentNotes[i]] = True
                #print(currentNotes[i])
        for i in range(len(currentNotes)):
            if not my_d[currentNotes[i]]:
                player.note_off(conversion(currentNotes[i]), 127)
    else:
        for i in range(len(currentNotes)):
            if not play_d2[currentNotes[i]]:
                player.note_on(conversion(currentNotes[i]), 127)
                play_d2[currentNotes[i]] = True
        for i in range(len(currentNotes)):
            if not my_d2[currentNotes[i]]:
                player.note_off(conversion(currentNotes[i]), 127)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands = 2)

my_d = {
    "A4": False,
    "B4": False,
    "C4": False,
    "D4": False,
    "E4": False,
    "F4": False,
    "G4": False,
}
play_d = {
    "A4": False,
    "B4": False,
    "C4": False,
    "D4": False,
    "E4": False,
    "F4": False,
    "G4": False,
}
my_d2 = {
    "A4": False,
    "B4": False,
    "C4": False,
    "D4": False,
    "E4": False,
    "F4": False,
    "G4": False,
}
play_d2 = {
    "A4": False,
    "B4": False,
    "C4": False,
    "D4": False,
    "E4": False,
    "F4": False,
    "G4": False,
}
pressedDown = [False, False, False, False, False, False, False]
pTime = 0
cTime = 0
iteration = 0

while True:
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    currentNotes = []
    currentNotes2 = []
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    #hands = detector.findHands(img, draw=False)

    
    buttonList = [Button([0, 300], "C4"), Button([30, 300], "C#4", ), Button([90, 300], "D#4"), Button([120, 300], "E4"), 
                Button([150, 300], "F4"), Button([180, 300], "F#4"), Button([210, 300], "G4"), Button([240, 300], "G#4"), 
                Button([270, 300], "A4"), Button([300, 300], "A#4"), Button([330, 300], "B4"), Button([360, 300], "C5"), 
                Button([390, 300], "C#5"), Button([420, 300], "D5"), Button([450, 300], "D#5"), Button([480, 300], "E5"), 
                Button([510, 300], "F5"), Button([540, 300], "F#5"), Button([570, 300], "G5"), Button([600, 300], "G#5"),
                Button([630, 300], "A5"), Button([660, 300], "A#5"), Button([690, 300], "B5"), Button([60, 300], "D4"),]
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
            if ((x < lmList1[4][0]<x+w and y < lmList1[4][1]<y+h) or (x < lmList1[8][0]<x+w and y < lmList1[8][1]<y+h) 
                or (x < lmList1[12][0]<x+w and y < lmList1[12][1]<y+h) or (x < lmList1[16][0]<x+w and y < lmList1[16][1]<y+h) 
                or (x < lmList1[20][0]<x+w and y < lmList1[20][1]<y+h)):
                #if (not pressedDown[i]):
                
                cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                my_d[button.text] = True    
                    
                currentNotes.append(button.text)

            else:
                my_d[button.text] = False
                play_d[button.text] = False

    if len(hands)==2:
        hand2 = hands[1]
        lmList2 = hand2["lmList"]

        for button in buttonList:

            x, y = button.pos
            w, h = button.size
            if ((x < lmList2[4][0]<x+w and y < lmList2[4][1]<y+h) or (x < lmList2[8][0]<x+w and y < lmList2[8][1]<y+h) 
                or (x < lmList2[12][0]<x+w and y < lmList2[12][1]<y+h) or (x < lmList2[16][0]<x+w and y < lmList2[16][1]<y+h) 
                or (x < lmList2[20][0]<x+w and y < lmList2[20][1]<y+h)):
                #if (not pressedDown[i]):
                     
                cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                my_d2[button.text] = True
                currentNotes2.append(button.text)

            else:
                my_d2[button.text] = False
                play_d2[button.text] = False
    iteration += 1
    if not ((len(currentNotes) == 0) and (len(currentNotes2) == 0)):
        if (i == len(buttonList)-1):
                print(currentNotes)
                print(currentNotes2)
                merger(currentNotes, 1)
                merger(currentNotes2, 2)
                #print (len(currentNotes))      
                #print (len(currentNotes2))   
    

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
         break
