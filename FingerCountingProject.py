import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# folderPath = "Images"
# myCalc = os.listdir(folderPath)
#
# overlayList = []
# for imPath in myCalc:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     overlayList.append(image)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

res = 0

currTime = time.time()

function = "add"

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Right Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Right 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if time.time() - currTime >= 2:
            # NONE UP (RESET)
            if fingers == [0, 0, 0, 0, 0]:
                res = 0
                print("RESET")

            # THUMB UP (ADD)
            elif fingers == [1, 0, 0, 0, 0]:
                function = "add"
                print("ADD")

            # PINKY UP (SUB)
            elif fingers == [0, 0, 0, 0, 1]:
                function = "sub"
                print("SUB")

            # THUMB & PINKY UP (MUL)
            elif fingers == [1, 0, 0, 0, 1]:
                function = "mul"
                print("MUL")

            # POINTER & PINKY UP (DIV)
            elif fingers == [0, 1, 0, 0, 1]:
                function = "div"
                print("DIV")

            else:
                totalFingers = fingers.count(1)

                if function == "add":
                    res += totalFingers
                elif function == "sub":
                    res -= totalFingers
                elif function == "mul":
                    res *= totalFingers
                elif function == "div":
                    res /= totalFingers

                function = "null"

            # print(res)
            currTime = time.time()

        # h, w, c = overlayList[0].shape
        # img[10:h+10, 10:w+10] = overlayList[0]

    cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(res), (25, 375), cv2.FONT_HERSHEY_PLAIN,
                10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # Exit window 49:20 Chapter 2
    if cv2.getWindowProperty('Image', 4) < 1:
        break
