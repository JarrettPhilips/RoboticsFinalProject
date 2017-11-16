'''
testing blob detection 
'''

import opencvmaster as cv
import numpy as np
import sys	

img = cv.imread(LandingPadCircles.png)

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

blobs = detector.detect(im)
for blob in blobs:
	print(blob)
