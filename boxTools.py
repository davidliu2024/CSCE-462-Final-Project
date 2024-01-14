import cv2
import imutils


def getMaskAndVal(frame, backSub, lower, upper, r):
	mask = cv2.GaussianBlur(frame, (15, 15),0)  
	hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	mask = backSub.apply(mask)     
	mask = cv2.dilate(mask, None)
	

	ret, mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	retFrame = cv2.bitwise_and(frame, frame, mask=mask)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		
		# only proceed if the radius meets a minimum size
		if r-1 < radius <= r+1:
			center = (x, y)
		return retFrame, center