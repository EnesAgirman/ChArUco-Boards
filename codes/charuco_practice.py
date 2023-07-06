import cv2 as cv
import numpy as np
from cv2 import aruco

xNum = 7    # The number of squares in the X direction
yNum = 5    # The number of squares in the Y direction

squareSize = 0.040 # The size of the squares. It is the length of one side
markerSize = 0.025 # The size of the aruco markers. It is the length of one side

markerDict = aruco.Dictionary_get(aruco.DICT_7X7_100 ) # The dictionary that we use for the aruco markers

imageSize = (7*120, 5*120)  # The size of the image of the charuco board

myGridBoard = cv.aruco.CharucoBoard.create(xNum, yNum, squareSize, markerSize, markerDict)  # The gridboard that includes the charuco board information

# myGridBoard.setIds( np.array([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]) ) # Assign the ID's of the aruco markers on the gridboard
# print(myGridBoard.ids)    # Display the id's of the aruco markers on the gridboard

myImage = myGridBoard.draw(outSize=imageSize)   # Generate an image of the charuco board using the gridboard

cv.imshow("My Image", myImage)  # Display the charuco board image


cv.waitKey(0)

print("\n\n Execution Completed \n\n")
