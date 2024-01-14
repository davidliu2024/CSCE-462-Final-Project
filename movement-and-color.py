# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
from playsound import playsound as pl
from colorCorrection import findHSV
from tools import findDistance

backSub = cv2.createBackgroundSubtractorMOG2(history=700)
lower, upper = findHSV()
print(lower, upper)

vs = VideoStream(src=0).start()
time.sleep(2.0)

pts = deque(maxlen=4)

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
	mask = cv2.GaussianBlur(frame1, (15, 15),0)  
	hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	mask = backSub.apply(mask)
	mask = cv2.dilate(mask, None)
	

	ret,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		
		# only proceed if the radius meets a minimum size
		if r-1 < radius <= r+1:
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			# cv2.circle(frame1, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			# pl("./beep.mp3")
				# x.start
			print(int(x), int(y))
	pts.appendleft(center)
			# cv2.circle(frame1, center, 5, (0, 0, 255), -1)
	for i in range(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		angle = findDistance(pts[i], pts[i-1])
		# if angle != 0:
		# 	print(angle, end=" ")
		# if i == len(pts)-1:
		# 	print()

	result = cv2.bitwise_and(frame1, frame1, mask=mask)
	result2 = cv2.bitwise_and(frame2, frame2, mask=mask)

	# cv2.rectangle(frame, a1, a2, (255,0,0), 2, 1)
	# cv2.rectangle(frame, b1, b2, (0,255,0), 2, 1)
	cv2.imshow("Frame", result)
	cv2.imshow("Frame", result2)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
vs.stop()
# close all windows
cv2.destroyAllWindows()