'''
	Abstract: Given a photo, analyzes contours to determine if the landing pad is in the image
	Dependencies: OpenCV 2 needs to be installed, written for Python 2.7
	
	Variable Adjustments: Depending on the desired environment, variables can be adjusted to accomadate different pads, accuracies, and environmental factors
	There are a lot of commented out print statements. Please do not remove them, they are SUPER useful.
	V4 is the new dark pad version (can be found on the repo). 
	V5 is a failed experiment, but comments with it's values have been left in just in case. Just ignore them for now
	
	Calling: This clearProgram can be called from either command line or just a function call.
	Image name is a string of the directory of the image. If they are in the same directory, this is just the image name.
	Please include the file type (e.g. ".jpg" or ".png")
	The true or false value is just whether you want the program to generate a visual output of it's work.
	It's really helpful for debugging, but doesn't affect the program otherwise.
		Command line: >python2 FindPad.py Imagename.png True/False
		Function call: findPad(imageName, True/False)

	Returns: return code, X-Coord of first possible landing pad center, Y-Coord of first possible landing pad center, Area of first possible landing pad center, List of all possible landing pad centers, List of all possible landing pad areas
	*All returned values are integers

	Return Code Key
	===============
	-1	| Error
	0	| No Pads Found
	1	| Single Primary Pad Found
	2	| Single Secondary Pad Found
	11	| Multiple Primary Pads Found
	12	| Multiple Secondary Pads Found	
'''

import numpy as np
import cv2 as cv
import sys
import math
import time

#########################################
#				Variables				#
#########################################
#Landing pad details
outerRingAreaRatio = 1.745 #Default is [1.745, V4], [1.749, V5]
innerRingAreaRatio = 1.339 #Default is [1.339, V4], [1.195, V5]
outerInnerRingAreaRatio = 3.506 #Default is [3.506, V4], [7.539, V5]
innerRingCircleAreaRatio = 13.019 #Default it [13.019, V4], [14.617, V5]

ringAreaRatioInaccuracyThreshold = 0.15 #Default is [0.025, iphone res], [0.07, drone res @ low altitude], [0.15, drone res @ high altitude]
centerPointLocationInaccuracyThreshold = 10.0 #In pixels (default is [20, iphone res], [10, drone res])

#Other CV adjustments
contourAreaMinimumThreshold = 250 #Contour areas will be discarded if they contain less than the threshold number of pixels (default is [1000, High Res], [100, Low Res])

proceduralMode = False
createVisualOutput = True
#########################################
#			Helper Functions			#
#########################################
def getContours(imageName):
	#Read in image, manipulate to allow cv to work
	image = cv.imread(imageName)
	grayscaleImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	ret, threshold = cv.threshold(grayscaleImage, 150, 255, 0) #image, lower bound, upper bound, no idea

	#Find edges
	im2, contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	#print contours

	return contours

def insertionSort(array, array2): #Sorts two arrays based on array 1
	for index in range(1, len(array)):
		currentContour = array2[index]
		currentvalue = array[index]
		position = index

		while position > 0 and array[position - 1] > currentvalue :
			array2[position] = array2[position - 1]
			array[position] = array[position - 1]
			position = position - 1

		array[position] = currentvalue
		array2[position] = currentContour
	return array, array2

def cleanAndSortContoursByArea(contours):
	print len(contours), "Total Contours"

	contourAreas = []
	contoursReduced = []
	for i in range(len(contours)):
		area = cv.contourArea(contours[i])

		if area >= contourAreaMinimumThreshold :
			contourAreas.append(area)
			contoursReduced.append(contours[i])

	contourAreasSorted, contoursSorted = insertionSort(contourAreas, contoursReduced)
	contourAreasSorted.reverse()
	contoursSorted.reverse()
	print len(contourAreasSorted), "Contours greater than", contourAreaMinimumThreshold, "pixels in area"


	return contourAreasSorted, contoursSorted

#Find the center of a given contour
def findCenterOfContour(contour):
	M = cv.moments(contour)
	cx = int(M['m10'] / M['m00'])
	cy = int(M['m01'] / M['m00'])
	return cx, cy

def searchForContourPairByAreaRatio(contourAreasSorted, contoursSorted, ratio, threshold):
	listOfAreaPairs = []
	listOfContourPairs = []

	for i in range(len(contourAreasSorted)) :
		for j in range(len(contourAreasSorted)) :
			if j != i :
				if areAreasSimilar(contourAreasSorted[i], contourAreasSorted[j], ratio, threshold) :
					listOfAreaPairs.append(contourAreasSorted[i])
					listOfAreaPairs.append(contourAreasSorted[j])

					listOfContourPairs.append(contoursSorted[i])
					listOfContourPairs.append(contoursSorted[j])

	return listOfAreaPairs, listOfContourPairs

def findAreasWithSharedCenter(outerRingListOfAreaPairs, outerRingListOfContourPairs, innerOuterRingListOfAreaPairs, innerOuterListOfContourPairs) :
	commonCenterPoints = []
	commonCenterPointsOuterAreas = []
	padFound = False

	for i in range(len(outerRingListOfContourPairs)) :
		for j in range(len(innerOuterListOfContourPairs)) :

			if outerRingListOfAreaPairs[i] != innerOuterRingListOfAreaPairs[j] :
				centerOfOuterRingX, centerOfOuterRingY = findCenterOfContour(outerRingListOfContourPairs[i])
				centerOfInnerRingX, centerOfInnerRingY = findCenterOfContour(innerOuterListOfContourPairs[j])

				if arePointsClose(centerOfOuterRingX, centerOfOuterRingY, centerOfInnerRingX, centerOfInnerRingY, centerPointLocationInaccuracyThreshold) :
					centerPoint = [centerOfOuterRingX, centerOfOuterRingY]
					pointIsUnique = True
					
					for k in range(len(commonCenterPoints)) :
						if arePointsClose(commonCenterPoints[k][0], commonCenterPoints[k][1], centerPoint[0], centerPoint[1], centerPointLocationInaccuracyThreshold) :
							pointIsUnique = False

					if pointIsUnique :
						'''
						print "= New Common Center Point Found ="
						print "OR:", outerRingListOfAreaPairs[i - 1], outerRingListOfAreaPairs[i], outerRingListOfAreaPairs[i + 1]
						print "OIR:", innerOuterRingListOfAreaPairs[j - 1], innerOuterRingListOfAreaPairs[j], innerOuterRingListOfAreaPairs[j + 1]
						print "Center:", centerPoint
						'''
						commonCenterPoints.append(centerPoint)
						commonCenterPointsOuterAreas.append(outerRingListOfAreaPairs[i])
						padFound = True

			j = j + 1
		i = i + 1

	return padFound, commonCenterPoints, commonCenterPointsOuterAreas

def areAreasSimilar(area1, area2, ratio, threshold):
	if (float(area1) / float(area2)) > (ratio - threshold) and (float(area1) / float(area2)) < (ratio + threshold) :
		return True
	return False

def arePointsClose(x1, y1, x2, y2, maximumDistance):
	distance = math.sqrt(math.pow((float(x1) - float(x2)), 2) + math.pow((float(y1) - float(y2)), 2))
	if distance <= maximumDistance :
		return True
	else :
		return False

#########################################
#			Primary Functions			#
#########################################
def findPad(imageName):
	start_time = time.time()
	returnCode = -1
	print "======================="

	#Get image, convert to B&W / find contours
	contours = getContours(imageName)

	#Sort contours by area (largest to smallest), remove outliers and clean data
	contourAreasSorted, contoursSorted = cleanAndSortContoursByArea(contours)
	#print contourAreasSorted

	#Search for outer ring by area ratio
	outerRingListOfAreaPairs, outerRingListOfContourPairs = searchForContourPairByAreaRatio(contourAreasSorted, contoursSorted, outerRingAreaRatio, ringAreaRatioInaccuracyThreshold)
	print len(outerRingListOfAreaPairs), "Possible Outer Rings"

	#Search for inner ring by area ratio
	innerOuterRingListOfAreaPairs, innerOuterListOfContourPairs = searchForContourPairByAreaRatio(contourAreasSorted, contoursSorted, outerInnerRingAreaRatio, ringAreaRatioInaccuracyThreshold)
	print len(innerOuterRingListOfAreaPairs), "Possible Inner Outer Ring Combinations"
	print len(outerRingListOfAreaPairs) * len(innerOuterRingListOfAreaPairs), "Total Combinations"
	print "-----------------------"
	'''
	print "outerRingListOfContourPairs"
	print outerRingListOfAreaPairs
	print "innerOuterListOfContourPairs"
	print innerOuterRingListOfAreaPairs
	'''

	#Check for shared center point	
	padFound, commonCenterPoints, commonCenterPointsOuterAreas = findAreasWithSharedCenter(outerRingListOfAreaPairs, outerRingListOfContourPairs, innerOuterRingListOfAreaPairs, innerOuterListOfContourPairs)
	if len(commonCenterPoints) > 1 :
		returnCode = 11
	
	#Check shared center point
	if padFound : #If true, return 1 and pixel coordinates
		print len(commonCenterPoints), "Possible Pad(s) Center Found"
		print commonCenterPoints
		returnCode = 1
	else : #If false, check if inner ring exists
		print "Full Pad Not Found. Conducting Search For Secondary Pad"
		#Search for inner ring by area ratio
		innerRingListOfAreaPairs, innerRingListOfContourPairs = searchForContourPairByAreaRatio(contourAreasSorted, contoursSorted, innerRingAreaRatio, ringAreaRatioInaccuracyThreshold)
		print len(innerRingListOfAreaPairs), "Possible Inner Rings"

		#Search for inner ring by area ratio
		innerRingCircleListOfAreaPairs, innerRingCircleListOfContourPairs = searchForContourPairByAreaRatio(contourAreasSorted, contoursSorted, innerRingCircleAreaRatio, ringAreaRatioInaccuracyThreshold)
		print len(innerOuterRingListOfAreaPairs), "Possible Inner Ring Circle Combinations"
		print len(outerRingListOfAreaPairs) * len(innerOuterRingListOfAreaPairs), "Total Combinations"
		print "-----------------------"

		secondaryPadFound, secondaryCommonCenterPoints, secondaryCommonCenterPointsOuterAreas = findAreasWithSharedCenter(innerRingListOfAreaPairs, innerRingListOfContourPairs, innerRingCircleListOfAreaPairs, innerRingCircleListOfContourPairs)
		if len(secondaryCommonCenterPoints) > 1 :
			returnCode = 12

		if secondaryPadFound : #If true, return 2 and cut drone engines
			print len(secondaryCommonCenterPoints), "Possible Secondary Pad(s) Found"
			print secondaryCommonCenterPoints
			padFound = True
			commonCenterPoints = secondaryCommonCenterPoints
			commonCenterPointsOuterAreas = secondaryCommonCenterPointsOuterAreas
			returnCode = 2
		else : #If false, return 0 and report no pad found
			print "Secondary Pad Not Found. No Pad Identified"
			returnCode = 0
			

	if createVisualOutput :
		#Create an output image for visual aid
		image = cv.imread(imageName)
		grayscaleImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
 		outputImage = cv.cvtColor(grayscaleImage, cv.COLOR_GRAY2BGR)
		cv.drawContours(outputImage, contoursSorted, -1, (0, 255, 255), 4)
		c = []
		c.append(contoursSorted[1])
		cv.drawContours(outputImage, c, -1, (255, 255, 0 ), 4)

		for i in range(len(commonCenterPoints)) :
			cv.line(outputImage, (0, commonCenterPoints[i][1]), (99999, commonCenterPoints[i][1]), (0, 225, 0), 5)
			cv.line(outputImage, (commonCenterPoints[i][0], 0), (commonCenterPoints[i][0], 99999), (0, 225, 0), 5)
			cv.circle(outputImage, (commonCenterPoints[i][0], commonCenterPoints[i][1]), 10, (255, 0, 0), -1)

		if padFound :
			cv.circle(outputImage, (commonCenterPoints[0][0], commonCenterPoints[0][1]), 10, (0, 0, 255), -1)
		
		#Draw lines through center of image
		imageHeight, imageWidth, channels = image.shape
		cv.line(outputImage, (0, imageHeight / 2), (99999, imageHeight / 2), (255, 0, 255), 5)
		cv.line(outputImage, (imageWidth / 2, 0), (imageWidth / 2, 99999), (255, 0, 255), 5)

		cv.imwrite("Output.jpg", outputImage)
		cv.waitKey(0)
		cv.destroyAllWindows()
	
	if padFound :
		print "Return:", returnCode, commonCenterPoints[0][0], commonCenterPoints[0][1], commonCenterPointsOuterAreas[0], commonCenterPoints, commonCenterPointsOuterAreas
		print "== Runtime Completed =="
		print("%s seconds" % (time.time() - start_time))
		print "======================="
		return returnCode, commonCenterPoints[0][0], commonCenterPoints[0][1], commonCenterPointsOuterAreas[0], commonCenterPoints, commonCenterPointsOuterAreas
	else : 
		print "Return:", returnCode, None, None, None, None, None
		print "== Runtime Completed =="
		print("%s seconds" % (time.time() - start_time))
		print "======================="
		return returnCode, None, None, None, None, None

#########################################
#				Procedural				#
#########################################
if proceduralMode :
	findPad(sys.argv[1], sys.argv[2])