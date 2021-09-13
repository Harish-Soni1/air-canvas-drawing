import cv2
import handTracking as htm
from collections import deque
import mediapipe as mp
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1100)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
markerPoints = [deque(maxlen=1024)]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) !=0:
        
        cv2.circle(img, lmList[8][1:], 15, (255, 0, 0), 4)

        fingers=[]
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers=fingers.count(1)

        if fingers.count(1) == 0:
            markerPoints = [deque(maxlen=1024)]

        if fingers[1] == 1 and fingers[2] == 0:
            if fingers[0] == 0:
                markerPoints.append(lmList[8][1:])

        elif fingers[1] == 1 and fingers[2] == 1:
            if len(markerPoints) > 1:
                for i in range(1, len(markerPoints)):
                    try:
                        if (lmList[8][1] - markerPoints[i][0])**2 + (lmList[8][2] - markerPoints[i][1])**2 <= 20**2:
                            markerPoints.pop(i)
                    except:
                        pass
        
        for i in range(2, len(markerPoints)):
            if len(markerPoints[i]) > 0:
                cv2.line(img, markerPoints[i-1], markerPoints[i-1], (255, 0 , 0), 25)

    cv2.imshow("Image", cv2.flip(img, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
