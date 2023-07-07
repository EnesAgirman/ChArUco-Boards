from types import NoneType
import cv2 as cv
import numpy as np
from cv2 import aruco
import time
import pickle
import glob

# https://github.com/kyle-bersani/opencv-examples/blob/master/CalibrationByCharucoBoard/CalibrateCamera.py

def readCharuco(aImage, aDict, aCharucoBoard):
    
    corners_all = [] # Corners discovered in all images processed
    ids_all = [] # Aruco ids corresponding to corners discovered
    image_size = None # Determined at runtime

    myImageGrayScale = cv.cvtColor(aImage, cv.COLOR_BGR2GRAY)
    myCorners, myIDs, _ = aruco.detectMarkers( image=myImageGrayScale, dictionary=aDict)
    
    aImage = aruco.drawDetectedMarkers(image=aImage, corners=myCorners) # add ids=myIDs to also sraw id's of aruco markers
    
    if myIDs is None:
        print("\nhehehhehee boooi\n")
    else:
        # if myIDs doesn't exist, it does this
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(markerCorners=myCorners,markerIds=myIDs,image=myImageGrayScale,board=aCharucoBoard,cameraMatrix=None, distCoeffs=None, minMarkers=1)
        
        corners_all.append(myCorners)
        ids_all.append(myIDs)
        
        
        # Draw the Charuco board we've detected to show our calibrator the board was properly detected
        aImage = aruco.drawDetectedCornersCharuco(
                image=aImage,
                charucoCorners=charuco_corners, charucoIds=charuco_ids ) # charucoIds=charuco_ids for displaying ids 
        
    
    
    
def playVideo(aDict, aCharucoBoard):
    myVid = cv.VideoCapture(0)

    while 0xFF != ord(' '):
        captureSuccessfull, myFrame = myVid.read()

        readCharuco(myFrame, aDict, aCharucoBoard)



        cv.imshow("My Video", myFrame)
        cv.waitKey(50)
        
        if cv.waitKey(1) & 0xFF == ord(' '):
            break

myDict = aruco.Dictionary_get(aruco.DICT_7X7_100 )

xNum = 7    # The number of squares in the X direction
yNum = 5    # The number of squares in the Y direction

squareSize = 0.02836 # The size of the squares. It is the length of one side
markerSize = 0.01772 # The size of the aruco markers. It is the length of one side

myDict = aruco.Dictionary_get(aruco.DICT_7X7_100 ) # The dictionary that we use for the aruco markers

imageSize = (7*120, 5*120)  # The size of the image of the charuco board

# The gridboard that includes the charuco board information
myGridBoard = cv.aruco.CharucoBoard.create(xNum, yNum, squareSize, markerSize, myDict)

playVideo(myDict, myGridBoard)



print("\n\n\nExecution Finished\n\n\n")

