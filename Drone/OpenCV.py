'''
	Drone OpenCV Code - Find landing pad and calculate drone's position in relation to it

	Command Line Arguements:
	>python OpenCV.py photoDirectory 
	
	Dependencies:
	- Place OpenCV library in same directory as python file
'''

import opencvmaster as cv
import numpy as np
import sys	


photoDirectory = sys.argv[1]
print("Running diagnostics on file:", photoDirectory)

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

def findPad(blobs):
	for i in blobs
	# make a dictionary with the coordinates of blobs as the key
	# and the key with 3 entries is the pad




#Calculate Distance to Pad
squareTrueSize = 17.78 #cm (7 inch)
circleTrueSize = 7.62  #cm (3 inch)

