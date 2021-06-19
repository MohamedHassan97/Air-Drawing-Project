import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import AiMouse as mouse
import subprocess




def virtual_painter_function(painter_flag):
    #######################
    brushThickness = 5
    eraserThickness = 100
    ########################


    folderPath = "K:/ASU/Second Term/dip/shaf3i part/Header"
    myList = os.listdir(folderPath)
    print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        print (image.shape)
        overlayList.append(image)
    print(len(overlayList))
    header = overlayList[0]
    drawColor = (255, 0, 133)

    #########################

    folderPath2 = "K:/ASU/Second Term/dip/shaf3i part/Header2"
    myList2 = os.listdir(folderPath2)

    print(myList2)
    overlayList2 = []
    for imPath in myList2:
        image2 = cv2.imread(f'{folderPath2}/{imPath}')
        print (image2.shape)

        overlayList2.append(image2)
    print(len(overlayList2))
    header2 = overlayList2[0]
    drawColor = (255, 0, 133)



    ############################
    cap = cv2.VideoCapture(0)
    print(cap.isOpened())
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = htm.handDetector(maxHands=2,trackCon = 0.9, detectionCon=0.9)
    xp, yp = 0, 0
    imgCanvas = np.zeros((720,1280, 3), np.uint8)
    counter =0
    runn= True
    while runn == True:
        if (painter_flag==True):
            # 1. Import image
            success, img = cap.read()
            img = cv2.flip(img, 1)


            # success, img = cap.read()
            # img = detector.findHands(img)

            # lmList, bbox = detector.findPosition(img)
            # if len(lmList) != 0:
            #     print(lmList[4])

            # 2. Find Hand Landmarks
            img = detector.findHands(img)
            lmList, _ = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                # xp,yp = 0,0
                print('here')
                print(lmList)

                # tip of index and middle fingers
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                # 3. Check which fingers are up
                fingers = detector.fingersUp()
                print(fingers)
                #############
                p_flag=True
                m_flag=False
                rec_flag=False

                # 3.5. If setting Mode - Two finger are up
                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    #print("setting Mode")
                    # # modes of operation
                    if 1160 <x1<1280:
                        if 150 < y1 < 250:
                            header2 = overlayList2 [0]
                            rec_flag=True

                            if (p_flag == True and rec_flag ==  True   ):

                                header2 = overlayList2 [1]
                                rec_flag=not(rec_flag)
                            elif (p_flag==True and rec_flag ==  False   ):


                                header2 = overlayList2 [0]

                            #subprocess.run("python3 VirtualPainter.py & python3 screenrecorder.py", shell=True)

                        elif (275 < y1 < 375):
                            header2 = header2
                            runn =False

                        elif 400 < y1 < 500:
                            header2 = overlayList2[0]
                            m_flag=False
                            p_flag=True

                        elif 525 < y1 < 625:
                            header2 = overlayList2[2]
                            m_flag=True
                            p_flag=False

                            mouse.AI_mouse_function(m_flag)





                ###############
                # 4. If Selection Mode - Two finger are up
                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    print("Selection Mode")
                    # # Checking for the click
                    if y1 < 125:
                        if 250 < x1 < 450:
                            header = overlayList[0]
                            drawColor = (255, 0, 255)
                        elif 550 < x1 < 750:
                            header = overlayList[1]
                            drawColor = (255, 0, 0)
                        elif 800 < x1 < 950:
                            header = overlayList[2]
                            drawColor = (0, 255, 0)
                        elif 1050 < x1 < 1200:
                            header = overlayList[3]
                            drawColor = (0, 0, 0)





                            #
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

                # 5. If Drawing Mode - Index finger is up
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    print("Drawing Mode")
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                    if drawColor == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                    else:
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                    xp, yp = x1, y1


                 #Clear Canvas when all fingers are up
                #if all (x == 0 for x in fingers[1:4]) and fingers[0] == 0:
                #    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
                ### for saving
                # if all (x == 0 for x in fingers[0:5]):
                #     imgCanvas = np.zeros((480, 640, 3), np.uint8)


                ## for saving
                if all (x == 0 for x in fingers[0:4]) and fingers[4] == 1:
                    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
                    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
                    if counter % 30 == 0:#30 fps
                        #cv2.imwrite('imgCanvas' + str(int(counter/30)) + '.jpg',imgCanvas)
                        cv2.imwrite('imgInv' + str(int(counter/30)) + '.jpg',imgInv)
                    counter = counter + 1


            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img,imgInv)
            img = cv2.bitwise_or(img,imgCanvas)


            # Setting the header image
            img[0:125, 0:1280] = header
            img[150:650, 1160:1280]=header2
            #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
            cv2.imshow("Image", img)
            cv2.imshow("Canvas", imgCanvas)
            cv2.imshow("Inv", imgInv)
            cv2.waitKey(1)



