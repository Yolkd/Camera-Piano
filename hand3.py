import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
from keyPress import Button
# from keySound import note
import threading
import pygame
import pygame.midi
import time
import sys
import mido
from mido import Message, MidiFile, MidiTrack


mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
track.append(Message('program_change', program=12, time=0))

pygame.init()
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

def convertMIDI(input):
    for i in range(len(input)):
        track.append(Message('note_on', note=input[i], velocity=64, time=0))
    track.append(Message('note_off', note=input[0], velocity=64, time=480))
    for i in range(1, len(input)):
        track.append(Message('note_off', note=input[i], velocity=64, time=0))

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
    convertedNotes = currentNotes.copy()
    for i in range(len(convertedNotes)):
        convertedNotes[i] = conversion(convertedNotes[i])
    if (len(convertedNotes)>0):
        convertMIDI(convertedNotes)
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
octave = 0
my_d = {
    "A"+str(4+octave): False,
    "B"+str(4+octave): False,
    "C"+str(4+octave): False,
    "D"+str(4+octave): False,
    "E"+str(4+octave): False,
    "F"+str(4+octave): False,
    "G"+str(4+octave): False,
    "A#"+str(4+octave): False,
    "C#"+str(4+octave): False,
    "D#"+str(4+octave): False,
    "F#"+str(4+octave): False,
    "G#"+str(4+octave): False,
    "A"+str(5+octave): False,
    "B"+str(5+octave): False,
    "C"+str(5+octave): False,
    "D"+str(5+octave): False,
    "E"+str(5+octave): False,
    "F"+str(5+octave): False,
    "G"+str(5+octave): False,
    "A#"+str(5+octave): False,
    "C#"+str(5+octave): False,
    "D#"+str(5+octave): False,
    "F#"+str(5+octave): False,
    "G#"+str(5+octave): False
}
play_d = {
    "A"+str(4+octave): False,
    "B"+str(4+octave): False,
    "C"+str(4+octave): False,
    "D"+str(4+octave): False,
    "E"+str(4+octave): False,
    "F"+str(4+octave): False,
    "G"+str(4+octave): False,
    "A#"+str(4+octave): False,
    "C#"+str(4+octave): False,
    "D#"+str(4+octave): False,
    "F#"+str(4+octave): False,
    "G#"+str(4+octave): False,
    "A"+str(5+octave): False,
    "B"+str(5+octave): False,
    "C"+str(5+octave): False,
    "D"+str(5+octave): False,
    "E"+str(5+octave): False,
    "F"+str(5+octave): False,
    "G"+str(5+octave): False,
    "A#"+str(5+octave): False,
    "C#"+str(5+octave): False,
    "D#"+str(5+octave): False,
    "F#"+str(5+octave): False,
    "G#"+str(5+octave): False
}
my_d2 = {
    "A"+str(4+octave): False,
    "B"+str(4+octave): False,
    "C"+str(4+octave): False,
    "D"+str(4+octave): False,
    "E"+str(4+octave): False,
    "F"+str(4+octave): False,
    "G"+str(4+octave): False,
    "A#"+str(4+octave): False,
    "C#"+str(4+octave): False,
    "D#"+str(4+octave): False,
    "F#"+str(4+octave): False,
    "G#"+str(4+octave): False,
    "A"+str(5+octave): False,
    "B"+str(5+octave): False,
    "C"+str(5+octave): False,
    "D"+str(5+octave): False,
    "E"+str(5+octave): False,
    "F"+str(5+octave): False,
    "G"+str(5+octave): False,
    "A#"+str(5+octave): False,
    "C#"+str(5+octave): False,
    "D#"+str(5+octave): False,
    "F#"+str(5+octave): False,
    "G#"+str(5+octave): False
}
play_d2 = {
    "A"+str(4+octave): False,
    "B"+str(4+octave): False,
    "C"+str(4+octave): False,
    "D"+str(4+octave): False,
    "E"+str(4+octave): False,
    "F"+str(4+octave): False,
    "G"+str(4+octave): False,
    "A#"+str(4+octave): False,
    "C#"+str(4+octave): False,
    "D#"+str(4+octave): False,
    "F#"+str(4+octave): False,
    "G#"+str(4+octave): False,
    "A"+str(5+octave): False,
    "B"+str(5+octave): False,
    "C"+str(5+octave): False,
    "D"+str(5+octave): False,
    "E"+str(5+octave): False,
    "F"+str(5+octave): False,
    "G"+str(5+octave): False,
    "A#"+str(5+octave): False,
    "C#"+str(5+octave): False,
    "D#"+str(5+octave): False,
    "F#"+str(5+octave): False,
    "G#"+str(5+octave): False
}
pressedDown = [False, False, False, False, False, False, False, False, False, False, False, False]
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

    buttonList = [Button([0, 300], "C"+str(4+octave)), Button([30, 300], "C#"+str(4+octave) ), Button([90, 300], "D#"+str(4+octave)), Button([120, 300], "E"+str(4+octave)), 
                Button([150, 300], "F"+str(4+octave)), Button([180, 300], "F#"+str(4+octave)), Button([210, 300], "G"+str(4+octave)), Button([240, 300], "G#"+str(4+octave)), 
                Button([270, 300], "A"+str(4+octave)), Button([300, 300], "A#"+str(4+octave)), Button([330, 300], "B"+str(4+octave)), Button([360, 300], "C"+str(5+octave)), 
                Button([390, 300], "C#"+str(5+octave)), Button([420, 300], "D"+str(5+octave)), Button([450, 300], "D#"+str(5+octave)), Button([480, 300], "E"+str(5+octave)), 
                Button([510, 300], "F"+str(5+octave)), Button([540, 300], "F#"+str(5+octave)), Button([570, 300], "G"+str(5+octave)), Button([600, 300], "G#"+str(5+octave)),
                Button([630, 300], "A"+str(5+octave)), Button([660, 300], "A#"+str(5+octave)), Button([690, 300], "B"+str(5+octave)), Button([60, 300], "D"+str(4+octave)),]
    for i in range(len((buttonList))):
             
             img = buttonList[i].keyCreate(img)


    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        fingerup = detector.fingersUp(hands[0])
        if (iteration%10==0):
            if (fingerup==[1, 1, 0, 1, 1]):
                mid.save('music.mid')
                sys.exit(-1)
            elif (fingerup==[0, 1, 0, 0, 0]):
                if (octave < 1):
                    octave+=1
                    currentNotes = []
                    currentNotes2 = []
                    my_d = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    play_d = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    my_d2 = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    play_d2 = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    time.sleep(0.2)
                    continue
            elif (fingerup==[0,1,1,0,0]):
                if (octave>-2):
                    octave-=1
                    currentNotes = []
                    currentNotes2 = []
                    my_d = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    play_d = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    my_d2 = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    play_d2 = {
                        "A"+str(4+octave): False,
                        "B"+str(4+octave): False,
                        "C"+str(4+octave): False,
                        "D"+str(4+octave): False,
                        "E"+str(4+octave): False,
                        "F"+str(4+octave): False,
                        "G"+str(4+octave): False,
                        "A#"+str(4+octave): False,
                        "C#"+str(4+octave): False,
                        "D#"+str(4+octave): False,
                        "F#"+str(4+octave): False,
                        "G#"+str(4+octave): False,
                        "A"+str(5+octave): False,
                        "B"+str(5+octave): False,
                        "C"+str(5+octave): False,
                        "D"+str(5+octave): False,
                        "E"+str(5+octave): False,
                        "F"+str(5+octave): False,
                        "G"+str(5+octave): False,
                        "A#"+str(5+octave): False,
                        "C#"+str(5+octave): False,
                        "D#"+str(5+octave): False,
                        "F#"+str(5+octave): False,
                        "G#"+str(5+octave): False
                    }
                    time.sleep(0.2)
                    continue

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
                #print(currentNotes)
                #print(currentNotes2)
                merger(currentNotes, 1)
                merger(currentNotes2, 2)
                #print (len(currentNotes))      
                #print (len(currentNotes2))   
    

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
         break
