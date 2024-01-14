# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
from playsound import playsound as pl
from colorCorrection import findHSV
from boxTools import getMaskAndVal

backSub = cv2.createBackgroundSubtractorMOG2(history=500)
lower, upper = findHSV()
print(lower, upper)

vs = VideoStream(src=0).start()
time.sleep(2.0)

def empty(a):
    pass

frame = vs.read()
bbox = cv2.selectROI(frame, False)
a1 = (int(bbox[0]), int(bbox[1]))
a2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
bbox = cv2.selectROI(frame, False)
b1 = (int(bbox[0]), int(bbox[1]))
b2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
cv2.destroyAllWindows()

cv2.namedWindow("TrackerBars")
cv2.createTrackbar("Radius", "TrackerBars", 0, 100, empty)

# keep looping
while True:
	r = cv2.getTrackbarPos("Radius", "TrackerBars")
	frame = vs.read()
	if frame is None:
		break

	# frame = imutils.resize(frame, width=600)
	frame1 = frame[a1[1]:a2[1], a1[0]:a2[0]]
	frame2 = frame[b1[1]:b2[1], b1[0]:b2[0]]
	retFrame1, center1 = getMaskAndVal(frame=frame1, backSub=backSub, lower=lower, upper=upper, r=r)
	retFrame2, center2 = getMaskAndVal(frame=frame2, backSub=backSub, lower=lower, upper=upper, r=r)
	print("Center1:", center1)
	print("Center2:", center2)

	# result1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
	# result2 = cv2.bitwise_and(frame2, frame2, mask=mask2)

	cv2.imshow("Frame", retFrame1)
	cv2.imshow("fram2", retFrame2)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
vs.stop()
# close all windows
cv2.destroyAllWindows()