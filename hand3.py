import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
from keyPress import Button
from keySound import note
import threading
import pygame
import pygame.midi
import time

from mido import Message, MidiFile, MidiTrack


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
        convert+=12
    return convert


def merger(currentNotes):
    for i in range(len(currentNotes)):
        player.note_on(conversion(currentNotes[i]), 127)
    time.sleep(1)
    for i in range(len(currentNotes)):
        player.note_off(conversion(currentNotes[i]), 127)


def playSound(note):
    #pygame.mixer.music.queue()
    pygame.mixer.music.load('Notes/'+note+'.mid')
    pygame.mixer.music.play(1)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands = 2)

pressedDown = [False, False, False, False, False, False, False]


while True:
    currentNotes = []
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


        i = -1
        for button in buttonList:
            i+=1


            x, y = button.pos
            w, h = button.size
            timer = threading.Thread(target = note, args = (button.text))
            if ((x < lmList1[4][0]<x+w and y < lmList1[4][1]<y+h) or (x < lmList1[8][0]<x+w and y < lmList1[8][1]<y+h) 
                or (x < lmList1[12][0]<x+w and y < lmList1[12][1]<y+h) or (x < lmList1[16][0]<x+w and y < lmList1[16][1]<y+h) 
                or (x < lmList1[20][0]<x+w and y < lmList1[20][1]<y+h)):
                #if (not pressedDown[i]):
                     
                pressedDown[i] = True
                cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                currentNotes.append(button.text)
                if(not pygame.mixer.music.get_busy()):
                    playSound(button.text)

            else:
                 pressedDown[i] = False
                

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

    if (i == len(buttonList)-1):
        merger(currentNotes)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
         break
