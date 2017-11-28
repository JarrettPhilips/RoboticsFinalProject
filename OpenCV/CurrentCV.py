import numpy as np
import cv2 as cv
import sys
import math
###################################
# Global Variables
###################################
#Runtime
commandLineArguementsEnabled = False

#Photo
photoWidth = 3024.0 #pixels
photoHeight = 4032.0
photoWidthFromOneMeter = 112.2 #cm (the width of the rectangle that the drone's camera captures from 100 cm above the ground)
photoHeightFromOneMeter = 113.5

#Drone
altitude = 100.0 #cm

###################################
# Helping Functions
###################################
def insertionSort(array):
	for index in range(1, len(array)):
		 currentvalue = array[index]
		 position = index

		 while position > 0 and array[position - 1] > currentvalue:
		     array[position] = array[position - 1]
		     position = position - 1

		 array[position] = currentvalue
	return array

#Find largest contour
def findLargestContour(contours):
	largestContourArea = 0.0
	largestContour = 0

	for x in contours :
		area = cv.contourArea(x)
		if area > largestContourArea :
			largestContourArea = area
			largestContour = x

	print "Largest Contour:", largestContour
	print "Largest Area:", largestContourArea
	return largestContour

#Find the center of a given contour
def findCenterOfContour(contour):
	M = cv.moments(contour)
	cx = int(M['m10'] / M['m00'])
	cy = int(M['m01'] / M['m00'])

	print "== Center of pad identified as =="
	print "Top-Left Origin X:", cx, "| Top-Left Origin Y:", cy
	return cx, cy

def areAreasSimilar(area1, area2):
	if (area1 / area2) > .9 and (area1 / area2) < 1.1 :
		return True
	return False

#Converts coordinates from a lop-left origin (aka photos) to a center origin
def convertCoordinates(x, y):
	centeredOriginPixelX = 0.0
	centeredOriginPixelY = 0.0
	centeredOriginPixelX = x - (photoWidth / 2)
	centeredOriginPixelY = -1 * (y - (photoHeight / 2))
	print "Center Origin X:", centeredOriginPixelX, "| Center Origin Y:", centeredOriginPixelY
	return centeredOriginPixelX, centeredOriginPixelY

#Calculates landing pad's position relative to drone (Is close, needs some tweaking to be more accurate)
def getLandingPadRelativePosition(x, y):
	landingPadRelativeX = (x / photoWidth) * (photoWidthFromOneMeter / 100.0) * (altitude)
	landingPadRelativeY = (y / photoHeight) * (photoHeightFromOneMeter / 100.0) * (altitude)
	print "Relative X:", landingPadRelativeX, "| Relative Y:", landingPadRelativeY
	return landingPadRelativeX, landingPadRelativeY

#Calculates the desired direction of travel (Drone is facing 0 radians, + is CCW)
def getHeadingAdjustment(x, y):
	deltaTheta = math.atan2(y, x) - 1.57079632675
	deltaTheta = deltaTheta * 180 / 3.1415926535 #Converts from radians to degrees
	print "Adjust heading", deltaTheta, "degrees"
	print "================================="
	return deltaTheta

def getContours(imageName):
	#Read in image, manipulate to allow cv to work
	print "Initializing"
	grayscaleImage = cv.cvtColor(imageName, cv.COLOR_BGR2GRAY)
	ret, threshold = cv.threshold(grayscaleImage, 220, 255, 0) #image, lower bound, upper bound, no idea

	#Find edges
	print "Finding Edges"
	im2, contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	#print contours

	return contours

def createVisualOutput(imageName):
	#Create an output image for visual aid
	contours = getContours(imageName)
	grayscaleImage = cv.cvtColor(imageName, cv.COLOR_BGR2GRAY)
	cx, cy = findCenterOfContour(findLargestContour(contours))

	print "Creating Visual Output"
	outputImage = cv.cvtColor(grayscaleImage, cv.COLOR_GRAY2BGR)
	cv.circle(outputImage, ((int)(photoWidth / 2), (int)(photoHeight / 2)), 10, (0, 255, 0), -1) #Circle in center of image
	cv.circle(outputImage, (cx, cy), 10, (255, 0, 0), -1) #Circle in center of pad
	cv.drawContours(outputImage, contours, -1, (0,255,255), 4)
	cv.imwrite('Output.jpg', outputImage)
	cv.waitKey(0)
	cv.destroyAllWindows()

###################################
# Main Call Functions
###################################
#Determines if the pad is visible, partially visible, or not visible in given image
#Returns -1 for not visible, 0 for partially visible, 1 for fully visible
def doesPadExist(imageName):
	contours = getContours(imageName)
	print "Searching for pad"

	contourAreas = []
	for i in range(len(contours)):
		area = cv.contourArea(contours[i])
		contourAreas.append(area)

	contourAreasSorted = insertionSort(contourAreas)
	contourAreasSorted.reverse()

	#With the sorted array, determine if contours 2/3 are close to the same value
	if areAreasSimilar(contourAreasSorted[1], contourAreasSorted[2]) :
		print "Pad has been found"
		return 1
	else :
		print "No pad found"
		return -1

def getCoordinatesOfCenterOfPad(imageName):
	contours = getContours(imageName)
	cx, cy = findCenterOfContour(findLargestContour(contours))
	x, y = convertCoordinates(cx, cy);
	padX, padY = getLandingPadRelativePosition(x, y)
	deltaTheta = getHeadingAdjustment(x, y)
	return padX, padY, deltaTheta

#Calls main in event of running program from command line
imageName = cv.imread(sys.argv[1])
print doesPadExist(imageName)
print getCoordinatesOfCenterOfPad(imageName)
createVisualOutput(imageName)
