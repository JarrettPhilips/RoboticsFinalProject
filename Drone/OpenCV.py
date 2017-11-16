'''
	**Uses python3**

	Drone OpenCV Code - Find landing pad and calculate drone's position in relation to it

	Command Line Arguements:
	>python OpenCV.py photoDirectory 
	
	Dependencies:
	- Place OpenCV library in same directory as python file
'''

import opencvmaster as cv
import numpy as np
import sys

########## Global Variables ##########
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
altitude = 0 #cm

#####################################################

photoDirectory = sys.argv[1]
print("Running diagnostics on file:", photoDirectory)

#####################################################

img = cv.imread(photoDirectory)

paramSquare = cv.SimpleBlobDetector_Params()
paramCircle = cv.SimpleBlobDetector_Params()

#Change thresholds
paramSquare.minThreshold = 10
paramSquare.maxThreshold = 200
paramCircle.minThreshold = 10
paramCircle.maxThreshold = 200
 
# Filter by Area
paramSquare.filterByArea = true
paramSquare.minArea = 200
paramCircle.filterByArea = true
paramCircle.minArea = 200
 
# Filter by Circularity
paramSquare.filterByCircularity = true
paramSquare.minCircularity = 0.75
paramCircle.filterByCircularity = true
paramCircle.minCircularity = 0.95

# Filter by Inertia
paramSquare.filterByInertia = true
paramSquare.minInertiaRatio = 0.75
paramCircle.filterByInertia = true
paramCircle.minInertiaRatio = 0.75


# Create Detectors
detectSquare = cv.SimpleBlobDetector(paramSquare)
detectSquare = cv.SimpleBlobDetector(paramCircle)

# Calculate Distance to Pad
def calculatePadLocation(innerCirclePixelOriginX, innerCirclePixelOriginY): #Returns x,y coordinates of pad RELATIVE to drone (cm)
	landingPadRelativeX = (innerCirclePixelOriginX / photoWidth) * (photoWidthFromOneMeter / 100) * (altitude)
	landingPadRelativeY = (innerCirclePixelOriginY / photoHeight) * (photoHeightFromOneMeter / 100) * (altitude)

	return landingPadRelativeX, landingPadRelativeY

def convertPhotoCoordinates(x, y): #converts coordinates from a lop-left origin (aka photos) to a center origin
	newX = x - (photoWidth / 2)
	newY = y - (photoHeight / 2)
	return newX, newY









