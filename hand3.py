import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8)

class Button():
    def __init__(self, pos, text, size = [22, 300]):
        self.pos = pos
        self.size = size
        self.text = text

    def keyCreate(self, img):
        x, y = self.pos
        w, h = self.size
        if (self.text[1] == '#'):
            cv2.rectangle(img, self.pos, (x+w, y+h), (0, 0, 0), cv2.FILLED)
        else:
            self.size = [30, 300]
            cv2.rectangle(img, self.pos, (x+w, y+h), (255, 255, 255), cv2.FILLED)
        # cv2.putText(img, self.text, (x + 50, y + 50), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

        return img
