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
# Functions
###################################
#Find largest contour
def findLargestContour(contours):
	largestContourArea = 0.0
	largestContour = 0

	for x in contours :
		area = cv. contourArea(x)
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
	print "Adjust heading", deltaTheta * 180 / 3.1415926535, "degrees"
	print "================================="
	return deltaTheta

###################################
# Main
###################################
def main():
	#Read in image, manipulate to allow cv to work
	print "Initializing"
	initialImage = "photo.jpg"
	if commandLineArguementsEnabled :
		initialImage = cv.imread(sys.argv[1])
	grayscaleImage = cv.cvtColor(initialImage, cv.COLOR_BGR2GRAY)
	ret, threshold = cv.threshold(grayscaleImage, 220, 255, 0) #image, lower bound, upper bound, no idea

	#Find edges
	print "Finding Edges"
	im2, contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	#print contours

	cx, cy = findCenterOfContour(findLargestContour(contours))
	x, y = convertCoordinates(cx, cy);
	padX, padY = getLandingPadRelativePosition(x, y)
	deltaTheta = getHeadingAdjustment(x, y)

	#Create an output image for visual aid
	print "Creating Visual Output"
	outputImage = cv.cvtColor(grayscaleImage, cv.COLOR_GRAY2BGR)
	cv.circle(outputImage, ((int)(photoWidth / 2), (int)(photoHeight / 2)), 10, (0, 255, 0), -1)
	cv.circle(outputImage, (cx, cy), 10, (255, 0, 0), -1)
	cv.drawContours(outputImage, contours, -1, (0,255,255), 4)
	cv.imwrite('Output.jpg', outputImage)
	cv.waitKey(0)
	cv.destroyAllWindows()

	return padX, padY, deltaTheta

#Calls main in event of running program from command line
commandLineArguementsEnabled = True
main()