from types import NoneType
import cv2 as cv
import numpy as np
from cv2 import aruco
import time
import pickle
import glob

def readCharuco(aImage, aDict, aCharucoBoard, aCount):
    
    corners_all = [] # Corners discovered in all images processed
    ids_all = [] # Aruco ids corresponding to corners discovered
    image_size = (720, 1280)

    myImageGrayScale = cv.cvtColor(aImage, cv.COLOR_BGR2GRAY)
    myCorners, myIDs, _ = aruco.detectMarkers( image=myImageGrayScale, dictionary=aDict)
    
    aImage = aruco.drawDetectedMarkers(image=aImage, corners=myCorners) # add ids=myIDs to also sraw id's of aruco markers
    
    if myIDs is None:
        # if myIDs doesn't exist, it does this
        print("\nhehehhehee boooi\n")
    else:
        # if myIDs exist, it does this
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(markerCorners=myCorners,markerIds=myIDs,image=myImageGrayScale,board=aCharucoBoard,cameraMatrix=None, distCoeffs=None, minMarkers=1)
        
        corners_all.append(charuco_corners)
        ids_all.append(charuco_ids)
        
        # corners_all = np.squeeze(corners_all)
        # myIDs = np.squeeze(myIDs)
        
        
        # Draw the Charuco board we've detected to show our calibrator the board was properly detected
        aImage = aruco.drawDetectedCornersCharuco(
                image=aImage,
                charucoCorners=charuco_corners, charucoIds=charuco_ids ) # charucoIds=charuco_ids for displaying ids 
        
        # Resizing the image
        # mySize = (aImage.shape[1]//2, aImage.shape[0]//2)
        # aImage = cv.resize(aImage, mySize, interpolation=cv.INTER_CUBIC)
        
        
        calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(charucoCorners=corners_all,
                                                                                           charucoIds=ids_all,
                                                                                           board=aCharucoBoard,
                                                                                           imageSize=image_size,
                                                                                           cameraMatrix=None,
                                                                                           distCoeffs=None)
        
        print(rvecs)
        cv.drawFrameAxes(image=aImage, cameraMatrix=cameraMatrix, distCoeffs=distCoeffs, rvec=rvecs[0], tvec=tvecs[0], length=0.3, thickness=3)
        
        print(rvecs)
        
        return aImage
        
        
        
        
        

   
def readFile(aDict, aCharucoBoard):
    myVid = cv.VideoCapture(0)
    
    count = -1

    for myFileName in glob.glob('images\webcam_calibration/*.jpg'):
        count = count+1
        myFrame = cv.imread(myFileName)
        
        cv.imshow(myFileName, myFrame)

        myFrame = readCharuco(myFrame, aDict, aCharucoBoard, count)

        cv.imshow("My Video" + str(count), myFrame)
        
        cv.waitKey(0)
        
        if cv.waitKey(1) & 0xFF == ord(' '):
            break

xNum = 7    # The number of squares in the X direction
yNum = 5    # The number of squares in the Y direction

squareSize = 0.02836 # The size of the squares. It is the length of one side
markerSize = 0.01772 # The size of the aruco markers. It is the length of one side

myDict = aruco.Dictionary_get(aruco.DICT_7X7_100 ) # The dictionary that we use for the aruco markers my images
# myDict = aruco.Dictionary_get(aruco.DICT_6X6_1000 ) # The dictionary that we use for the aruco markers for testCase image

imageSize = (7*120, 5*120)  # The size of the image of the charuco board

# The gridboard that includes the charuco board information
myGridBoard = cv.aruco.CharucoBoard.create(xNum, yNum, squareSize, markerSize, myDict)

readFile(myDict, myGridBoard)

cv.waitKey(0)

print("\n\n\nExecution Finished\n\n\n")









""" 
myPath = "images\webcam_calibration"

for filename in glob.glob('images\webcam_calibration/*.jpg'):
    cv.imshow(filename, cv.imread(filename))



 """





