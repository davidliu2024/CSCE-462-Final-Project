import cv2
import numpy as np
from time import sleep

def empty(a):
    pass

def findHSV():
    cap = cv2.VideoCapture(0)
    sleep(2)
    

    cv2.namedWindow("TrackerBars")
    cv2.createTrackbar("Hue Min", "TrackerBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackerBars", 179, 179, empty)

    cv2.createTrackbar("Sat Min", "TrackerBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackerBars", 255, 255, empty)

    cv2.createTrackbar("Val Min", "TrackerBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackerBars", 255, 255, empty)


    

    while True:
        ret, img = cap.read()
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("Hue Min", "TrackerBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackerBars")

        s_min = cv2.getTrackbarPos("Sat Min", "TrackerBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackerBars")

        v_min = cv2.getTrackbarPos("Val Min", "TrackerBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackerBars")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # print(lower, upper)

        mask = cv2.inRange(imgHSV, lower, upper)

        result = cv2.bitwise_and(img, img, mask=mask)

        # cv2.imshow("original", img)
        # cv2.imshow("HSV", imgHSV)
        # cv2.imshow("mask", mask)
        cv2.imshow("result", result)
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            cv2.destroyAllWindows()
            return lower, upper
        # 79, 49, 86, 102, 206, 255