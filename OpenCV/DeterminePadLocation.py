'''
	Takes data from FindPad.py and calculates the pad's location relative to the drone in real space
'''

import numpy as np
import cv2 as cv
import sys
import math
import FindPad

#########################################
#				Variables				#
#########################################
#Photo
photoWidth = 3024.0 #pixels
photoHeight = 4032.0
photoWidthFromOneMeter = 112.2 #cm (the width of the rectangle that the drone's camera captures from 100 cm above the ground)
photoHeightFromOneMeter = 113.5

#Drone
altitude = 0.0 #cm

#Image (not photo)
areaOfLandingSquareInPixelsAtBaseAltitudeCentimeters = 0.0
baseAltitude = 0.0
#areaOfLandingSquareInPixels = 0.0

#########################################
#			Helper Functions			#
#########################################
#Converts coordinates from a lop-left origin (aka photos) to a center origin
def convertCoordinates(x, y) :
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
def getHeadingAdjustment(x, y) :
	deltaTheta = math.atan2(y, x) - 1.57079632675
	deltaTheta = deltaTheta * 180 / 3.1415926535 #Converts from radians to degrees
	print "Adjust heading", deltaTheta, "degrees"
	print "================================="
	return deltaTheta

def updateAltitude(areaOfLandingSquareInPixels) :
	print "Updating altitude based on pad size"
	return math.abs(math.sqrt(areaOfLandingSquareInPixels) - math.sqrt(areaOfLandingSquareInPixelsAtBaseAltitudeCentimeters)) * baseAltitude


#########################################
#			Primary Functions			#
#########################################
def getCoordinatesOfCenterOfPad(topLeftPixelX, topLeftPixelY, areaOfLandingSquareInPixels) :
	updateAltitude()
	centeredPixelX, centeredPixelY = convertCoordinates(topLeftPixelX, topLeftPixelY);
	padX, padY = getLandingPadRelativePosition(x, y)
	deltaTheta = getHeadingAdjustment(x, y)
	return padX, padY, deltaTheta

def callFindPadThenGetCoordinatesOfCenterOfPad() :
	FindPad.main("testingimages/padv4i5.jpg", True)

#########################################
#				Procedural				#
#########################################
callFindPadThenGetCoordinatesOfCenterOfPad()
