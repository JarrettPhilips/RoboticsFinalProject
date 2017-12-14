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
#Photo (pixels)
photoHeight = 1088.0 #default [1088.0, drone], [3024.0, iPhone]
photoWidth = 1920.0 #default [1920.0, drone], [4032.0, iPhone]
#cm (the width of the rectangle that the drone's camera captures from 100 cm above the ground)
photoHeightFromOneMeter = 112.2 #default [], [112.2, iPhone]
photoWidthFromOneMeter = 113.5 #default [], [113.5, iPhone]

#Image (not photo)
areaOfLandingSquareInPixelsAtBaseAltitude = 63857.5 #Pixels
baseAltitude = 74.0 #cm

#Other
commandLineEnabled = True

#########################################
#			Helper Functions			#
#########################################
#Converts coordinates from a lop-left origin (aka photos) to a center origin
def convertCoordinates(x, y) :
	centeredOriginPixelX = 0.0
	centeredOriginPixelY = 0.0
	centeredOriginPixelX = x - (photoWidth / 2)
	centeredOriginPixelY = (-1 * y) + (photoHeight / 2)
	#print photoHeight, photoWidth
	return centeredOriginPixelX, centeredOriginPixelY

#Calculates landing pad's position relative to drone (Is close, needs some tweaking to be more accurate)
def getLandingPadRelativePosition(x, y, altitude):
	landingPadRelativeX = (float(x) / photoWidth) * (photoWidthFromOneMeter / 100.0) * (altitude)
	landingPadRelativeY = (float(y) / photoHeight) * (photoHeightFromOneMeter / 100.0) * (altitude)
	return landingPadRelativeX, landingPadRelativeY

#Calculates the desired direction of travel (Drone is facing 0 radians, + is CCW)
def getHeadingAdjustment(xi, yi) :
	x, y = rotatePoint((xi, yi), -1.57079632679) #Rotates 90 degrees so the trig function uses the drone's coordinate space
	deltaTheta = math.atan2(y, x) #Finds angle
	
	'''
	print xi, yi
	print x, y
	print deltaTheta
	'''

	deltaTheta = deltaTheta * 180 / 3.1415926535 #Converts from radians to degrees
	return deltaTheta

def rotatePoint(point, angle): #Radians
    ox = 0
    oy = 0
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def updateAltitude(areaOfLandingSquareInPixels) :
	#return math.fabs(math.sqrt(float(areaOfLandingSquareInPixels)) / math.sqrt(float(areaOfLandingSquareInPixelsAtBaseAltitude))) * baseAltitude
	return math.fabs((math.sqrt(float(areaOfLandingSquareInPixelsAtBaseAltitude)) / math.sqrt(float(areaOfLandingSquareInPixels))) * baseAltitude)
	#return math.fabs(18722 / math.sqrt(float(areaOfLandingSquareInPixels)))

#########################################
#			Primary Functions			#
#########################################
def getCoordinatesOfCenterOfPad(topLeftPixelX, topLeftPixelY, areaOfLandingSquareInPixels) :
	altitude = updateAltitude(areaOfLandingSquareInPixels)
	print "Altitude Estimated to be", altitude, "cm"
	centeredPixelX, centeredPixelY = convertCoordinates(topLeftPixelX, topLeftPixelY)
	print "Center Origin X:", centeredPixelX, "| Center Origin Y:", centeredPixelY
	padX, padY = getLandingPadRelativePosition(centeredPixelX, centeredPixelY, altitude)
	distance = math.sqrt(math.pow(padX, 2) + math.pow(padY, 2))
	print "Relative X:", padX, "| Relative Y:", padY
	print "Distance:", distance
	deltaTheta = getHeadingAdjustment(centeredPixelX, centeredPixelY)
	print "Adjust heading", deltaTheta, "degrees"
	print "======================="
	#return padX, padY, deltaTheta
	return altitude, deltaTheta, distance

def callFindPadThenGetCoordinatesOfCenterOfPad(imageName) :
	image = cv.imread(imageName)
	global photoHeight
	global photoWidth
	photoHeight, photoWidth, channels = image.shape

	returnCode, x, y, area, allCenters, allAreas = FindPad.findPad(imageName)
	print "Calculating distance to pad | x:", x, "| y:", y, " | area:", area, "|"
	print "X-Axis:", photoHeight / 2, "Y-Axis", photoWidth / 2
	if returnCode == 1 or returnCode == 2 :
		altitude, deltaTheta, distance = getCoordinatesOfCenterOfPad(x, y, area)
		print "Return:", altitude, deltaTheta, distance
		return altitude, deltaTheta, distance
	else :
		print "Return:", -1
		return -1

#########################################
#				Procedural				#
#########################################
if commandLineEnabled :
	callFindPadThenGetCoordinatesOfCenterOfPad(sys.argv[1])
