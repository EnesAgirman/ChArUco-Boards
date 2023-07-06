import cv2 as cv
import numpy as np
from cv2 import aruco
import time
import pickle
import glob

def readCharuco(aImage, aDict, aCharucoBoard):
    myImageGrayScale = cv.cvtColor(aImage, cv.COLOR_BGR2GRAY)
    myCorners, myIDs, _ = aruco.detectMarkers( image=myImageGrayScale, dictionary=aDict)
    
    aImage = aruco.drawDetectedMarkers(image=aImage, corners=myCorners)
    
    # response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(markerCorners=myCorners,markerIds=myIDs,image=myImageGrayScale,board=aCharucoBoard)

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

squareSize = 0.040 # The size of the squares. It is the length of one side
markerSize = 0.025 # The size of the aruco markers. It is the length of one side

myDict = aruco.Dictionary_get(aruco.DICT_7X7_100 ) # The dictionary that we use for the aruco markers

imageSize = (7*120, 5*120)  # The size of the image of the charuco board

# The gridboard that includes the charuco board information
myGridBoard = cv.aruco.CharucoBoard.create(xNum, yNum, squareSize, markerSize, myDict)

playVideo(myDict, myGridBoard)



print("\n\n\nExecution Finished\n\n\n")

