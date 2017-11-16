'''
	**Uses python3**

	Drone OpenCV Code - Find landing pad and calculate drone's position in relation to it

	Command Line Arguements:
	>python OpenCV.py photoDirectory, altitude (cm)
	
	Dependencies:
	- Place OpenCV library in same directory as python file
'''

import numpy as np
import sys	
import cv2 as cv

#####################################################
'''				 	  Variables			  	      '''
#####################################################
#Landing Pad
innerCircleTrueRadius = 2.54 #cm (1 inch)
middleCircleTrueRadius = 7.62 #cm (3 inch)
outerCircleTrueRadius = 15.24 #cm (6 inch)

#Photo
photoWidth = 640 #pixels
photoHeight = 360
photoWidthFromOneMeter = 187.1 #cm (the width of the rectangle that the drone's camera captures from 100 cm above the ground)
photoHeightFromOneMeter = 101.2

#Drone
altitude = 0.0 #cm

#####################################################
'''				 	  Functions			  	  	  '''
#####################################################

def getCoordinates(photoDirectory, altitude):
	print("Running diagnostics on file:", photoDirectory)
	print("Altitude:", altitude)

	photoX, photoY = findPad(detectBlobs(photoDirectory))
	print("PhotoX:", photoX, "| PhotoY:", photoY)
	pixelX, pixelY = convertPhotoCoordinates(photoX, photoY)
	print("PixelX:", pixelX, "| PixelY:", pixelY)
	relativeX, relativeY = calculatePadLocation(pixelX, pixelY)
	print("RelativeX:", relativeX, "| RelativeY:", relativeY)

	return relativeX, relativeY

def detectBlobs(path):
	img = cv.imread(path)

	paramCircle = cv.SimpleBlobDetector_Params()

	#Change thresholds
	paramCircle.minThreshold = 10
	paramCircle.maxThreshold = 200
	 
	# Filter by Area
	#paramCircle.filterByArea = true
	#paramCircle.minArea = 200
	 
	# Filter by Circularity
	paramCircle.filterByCircularity = True
	paramCircle.minCircularity = 0.90

	# Filter by Inertia
	paramCircle.filterByInertia = True
	paramCircle.minInertiaRatio = 0.75


	# Create Detectors
	detector1 = cv.SimpleBlobDetector_create(paramCircle)

	blobs = detector1.detect(img)
	return blobs

def findPad(blobs): #returns x, y coordinates (photo coordinates)
	#for i in blobs
	# make a dictionary with the coordinates of blobs as the key
	# and the key with 3 entries is the pad
	print("Hello World")
	return 0, 0


#Returns x,y coordinates of pad RELATIVE to drone (cm)
def calculatePadLocation(innerCirclePixelOriginX, innerCirclePixelOriginY): 
	landingPadRelativeX = (innerCirclePixelOriginX / photoWidth) * (photoWidthFromOneMeter / 100) * (altitude)
	landingPadRelativeY = (innerCirclePixelOriginY / photoHeight) * (photoHeightFromOneMeter / 100) * (altitude)
	return landingPadRelativeX, landingPadRelativeY

#Converts coordinates from a lop-left origin (aka photos) to a center origin
def convertPhotoCoordinates(x, y): 
	newX = x - (photoWidth / 2)
	newY = y - (photoHeight / 2)
	return newX, newY

#####################################################
'''				 Procedural / Main			  	  '''
#####################################################

getCoordinates("photo.jpg", 30)