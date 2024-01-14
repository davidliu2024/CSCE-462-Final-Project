# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from playsound import playsound as pl
from colorCorrection import findHSV
import picamera as PiCamera

backSub = cv2.createBackgroundSubtractorMOG2()

lower, upper = findHSV()
print(lower, upper)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points


pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

frame = vs.read()
bbox = cv2.selectROI(frame, False)
a1 = (int(bbox[0]), int(bbox[1]))
a2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
bbox = cv2.selectROI(frame, False)
b1 = (int(bbox[0]), int(bbox[1]))
b2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

# keep looping
while True:

	# print(lower, upper)
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	# frame = imutils.resize(frame, width=600)
	frame1 = frame[a1[1]:a2[1], a1[0]:a2[0]]
	frame2 = frame[b1[1]:b2[1], b1[0]:b2[0]]
	mask = cv2.GaussianBlur(frame1, (15, 15),0)  
	hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	mask = backSub.apply(mask)     
	mask = cv2.dilate(mask, None)
	

	ret,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	# mask = cv2.bitwise_and(frame1, frame1, mask=mask)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# print(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			# cv2.circle(frame1, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			pl("./beep.mp3")
				# x.start
			print(int(x), int(y))
			# cv2.circle(frame1, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)

		# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		# cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	result = cv2.bitwise_and(frame1, frame1, mask=mask)
	# cv2.imwrite(frame, result2)


	# cv2.rectangle(frame, a1, a2, (255,0,0), 2, 1)
	# cv2.rectangle(frame, b1, b2, (0,255,0), 2, 1)
	cv2.imshow("Frame", result)
	
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()