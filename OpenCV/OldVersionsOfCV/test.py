'''
testing blob detection 
'''

import cv2 as cv
import numpy as np
import sys	

img = cv.imread("LandingPadCircles.png")

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
for blob in blobs:
	print(blob)
