import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8)

class Button():
    def __init__(self, pos, text, size=[100,100]):
        self.pos = pos
        self.size = size
        self.text = text

    def keyCreate(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text, (x + 25, y + 25), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        return img