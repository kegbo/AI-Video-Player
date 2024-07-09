# Importing Libraries 
import cv2 
from cvzone.HandTrackingModule import HandDetector
 
import sys
cap = cv2.VideoCapture(0) 
detector = HandDetector(detectionCon=0.6, maxHands= 100)

oldvalue = "0"

while cap.isOpened(): 
	# Read video frame by frame 
	ret, img = cap.read()
	if(ret ==True):
		hands, img = detector.findHands(img)
		#print(len(hands))
  
		num = str(len(hands))
		if(num != oldvalue):
			sys.stdout.write(num)
			sys.stdout.flush()
		oldvalue = num

		cv2.imshow('Image', img) 
		if cv2.waitKey(1) & 0xff == ord('q'): 
			break
