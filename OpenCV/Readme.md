# Find Pad CV Program #

### Abstract: ###
Given a photo, analyzes contours to determine if the landing pad is in the image.

### Dependencies ###
- OpenCV 2 needs to be installed
- Uses Python 2.7

### Variable Adjustments ###
Depending on the desired environment, variables can be adjusted to accomadate different pads, accuracies, and environmental factors. Default settings for a few common runtimes have been included in comments.
- V4 is the new dark pad version (can be found on the repo). 
- V5 is a failed experiment, but comments with it's values have been left in just in case. Just ignore them for now

### Running ###
This Program can be called from either command line or just a function call. 

Image name is a string of the directory of the image. If they are in the same directory, this is just the image name. Please include the file type (e.g. ".jpg" or ".png")

The true or false value is just whether you want the program to generate a visual output of it's work. It's really helpful for debugging, but doesn't affect the program otherwise.
  
  Command line: `>python2 FindPad.py Imagename.png True/False`
  
  Function call: `findPad(imageName, True/False)`

### Returned Values ###
Returns: `return code, X-Coord of first possible landing pad center, Y-Coord of first possible landing pad center, List of all possible landing pad centers`

If multiple pads are found, it will first return the largest potential pad, then the entire array of possible pads. This will  be marked in the return code.

All returned values are integers.

##### Return Code Key #####
| Code  | Meaning                         |
|-------|:--------------------------------|
| `-1`	| Error                           |
| `0`	  | No Pads Found                   |
| `1`	  | Single Primary Pad Found        |
| `2`   | Single Secondary Pad Found      |
| `11`	| Multiple Primary Pads Found     |
| `12`	| Multiple Secondary Pads Found	  |
