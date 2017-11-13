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

#Calculate Distance to Pad
squareTrueSize = 17.78 #cm (7 inch)
circleTrueSize = 7.62  #cm (3 inch)

