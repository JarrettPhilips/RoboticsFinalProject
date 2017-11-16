'''
	**Uses python3**

	Drone OpenCV Code - Find landing pad and calculate drone's position in relation to it

	Command Line Arguements:
	>python OpenCV.py photoDirectory, altitude (cm)
	
	Dependencies:
	- Place OpenCV library in same directory as python file
'''

import opencvmaster as cv
import numpy as np
import sys	

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
'''				 Procedural / Main			  	  '''
#####################################################

photoDirectory = sys.argv[1]
altitude = sys.argv[2]
print("Running diagnostics on file:", photoDirectory)

photoX, photoY = findPad(detectBlobs(photoDirectory))
print("PhotoX:", photoX, "| PhotoY:", photoY)
pixelX, pixelY = convertPhotoCoordinates(photoX, photoY)
print("PixelX:", PixelX, "| PixelY:", pixelY)
relativeX, relativeY = calculatePadLocation(pixelX, pixelY)
print("RelativeX:", relativeX, "| RelativeY:", relativeY)

return relativeX, relativeY

#####################################################
'''				 	  Functions			  	  	  '''
#####################################################
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
	paramCircle.filterByCircularity = true
	paramCircle.minCircularity = 0.90

	# Filter by Inertia
	paramCircle.filterByInertia = true
	paramCircle.minInertiaRatio = 0.75


	# Create Detectors
	detector1 = cv.SimpleBlobDetector(paramCircle)

	blobs = detector.detect(img)
	return blobs

def findPad(blobs): #returns x, y coordinates (photo coordinates)
	for i in blobs
	# make a dictionary with the coordinates of blobs as the key
	# and the key with 3 entries is the pad

def calculatePadLocation(innerCirclePixelOriginX, innerCirclePixelOriginY): #Returns x,y coordinates of pad RELATIVE to drone (cm)
	landingPadRelativeX = (innerCirclePixelOriginX / photoWidth) * (photoWidthFromOneMeter / 100) * (altitude)
	landingPadRelativeY = (innerCirclePixelOriginY / photoHeight) * (photoHeightFromOneMeter / 100) * (altitude)

	return landingPadRelativeX, landingPadRelativeY

def convertPhotoCoordinates(x, y): #converts coordinates from a lop-left origin (aka photos) to a center origin
	newX = x - (photoWidth / 2)
	newY = y - (photoHeight / 2)
	return newX, newY









