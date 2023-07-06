import cv2 as cv
import numpy as np
from cv2 import aruco
import time

def findArucoMarkers(aImage, aDict):
    myImageGrayScaled = cv.cvtColor(aImage, cv.COLOR_BGR2GRAY)
    arucoParameters = aruco.DetectorParameters_create()
    boundaryBoxes, myID, rejectedImages = aruco.detectMarkers(myImageGrayScaled, aDict, parameters=arucoParameters)
    print(myID)
    
    aruco.drawDetectedMarkers(aImage, boundaryBoxes, myID)
    return (boundaryBoxes, myID, rejectedImages)

def readCharucoBoard(aDict, aImage, aBoard):
    myImageGrayScaled = aImage
    markerCorners, markerIds, rejected = cv.aruco.detectMarkers(myImageGrayScaled, aDict)
    myCharucoCorners, myCharucoIds,  = cv.aruco.interpolateCornersCharuco(markerCorners, markerIds, myImageGrayScaled, aBoard)
    cv.aruco.drawDetectedCornersCharuco(aImage, myCharucoCorners, myCharucoIds)



def playVideo():
    myVid = cv.VideoCapture(0)
    myDict = aruco.Dictionary_get(aruco.DICT_7X7_100)
    
    myGridBoard = cv.aruco.CharucoBoard.create(7, 5, 0.04, 0.025, myDict)
    
    # ChAruco board variables
    CHARUCOBOARD_ROWCOUNT = 7
    CHARUCOBOARD_COLCOUNT = 5 
    ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_5X5_1000)

# Create constants to be passed into OpenCV and Aruco methods
    CHARUCO_BOARD = aruco.CharucoBoard_create(
        squaresX=CHARUCOBOARD_COLCOUNT,
        squaresY=CHARUCOBOARD_ROWCOUNT,
        squareLength=0.04,
        markerLength=0.02,
        dictionary=ARUCO_DICT)
    
    corners_all = [] # Corners discovered in all images processed
    ids_all = [] # Aruco ids corresponding to corners discovered
    image_size = None # Determined at runtime

    while 0xFF != ord(' '):
        captureSuccessfull, myFrame = myVid.read()
        
        gray = cv.cvtColor(myFrame, cv.COLOR_BGR2GRAY)
        
        corners, ids, _ = aruco.detectMarkers(image=gray,dictionary=myDict)
        
        img = aruco.drawDetectedMarkers(image=img, corners=corners)
        
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,
            board=CHARUCO_BOARD)
        
        if response > 20:
            # Add these corners and ids to our calibration arrays
            corners_all.append(charuco_corners)
            ids_all.append(charuco_ids)
            
            # Draw the Charuco board we've detected to show our calibrator the board was properly detected
            img = aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)
       
        # If our image size is unknown, set it now
        if not image_size:
            image_size = gray.shape[::-1]
    
            # Reproportion the image, maxing width or height at 1000
            proportion = max(img.shape) / 1000.0
            img = cv.resize(img, (int(img.shape[1]/proportion), int(img.shape[0]/proportion)))
            # Pause to display each image, waiting for key press
            cv.imshow('Charuco board', img)
            cv.waitKey(0)
        else:
            print("Not able to detect a charuco board in image")

        
        
        
        
        
        
        
        
        # boundaryBoxes, myID, rejectedImages = findArucoMarkers(myFrame, myDict )
        readCharucoBoard( myDict, myFrame, myGridBoard )
        cv.imshow("My Video", myFrame)
        cv.waitKey(50)
        
        if cv.waitKey(1) & 0xFF == ord(' '):
            break    

playVideo()



print("\n\n\nExecution Finished\n\n\n")