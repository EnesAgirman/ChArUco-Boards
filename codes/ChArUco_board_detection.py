from types import NoneType
import cv2 as cv
from cv2 import*
import numpy as np
from cv2 import aruco
import glob


# ChArUco_board_detection
class CharucoBoard():
    """
    Helper class for detecting Charuco boards.
    """
    def __init__(self, aImage, aDict, aCharucoBoard) -> None:
        """
        Arguments
            aImage: the image of the charuco board. It is of type 
            aDict: the dictionary which is used for the aruco markers on the charuco board
            aCharucoBoard: the charuco board that we are taking the image of. It is of the type cv2.aruco.CharucoBoard 
        """
        self.image = aImage
        self.dict = aDict
        self.charucoBoard = aCharucoBoard
        
        self.corners_all = [] # Corners discovered in all images processed
        self.ids_all = [] # Aruco ids corresponding to corners discovered
        
        if self.image is not None:
            self.image_size = (self.image.shape[0], self.image.shape[1])
            self.grayScaledImage = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
            self.corners, self.ids, _ = aruco.detectMarkers( image=self.grayScaledImage, dictionary=self.dict)
            if (self.corners is not None) & (self.ids is not None):
                self.image = aruco.drawDetectedMarkers(image=self.image, corners=self.corners) # add ids=self.ids to also draw id's of aruco markers
                self.ReadCharuco(self.ids, self.corners, self.grayScaledImage, self.charucoBoard, self.corners_all, self.ids_all)
                self.cameraMatrix, self.distCoeffs, self.rvecs, self.tvecs = self.FindIntrinsicAndExtrinsicCoefficients(self.corners_all,
                                                                                                                        self.ids_all, 
                                                                                                                        self.charucoBoard, 
                                                                                                                        self.image_size)
                self.image = self.drawFrameAxesOnImage(self.image, 
                                                    self.cameraMatrix, 
                                                    self.distCoeffs, 
                                                    self.rvecs, 
                                                    self.tvecs, 
                                                    aLength=0.3, 
                                                    aThickness=3)


    def ReadCharuco(self, aIds, aCorners, aImageGrayScale, aCharucoBoard, aCornersAll, aIdsAll):
        """ reads the image and finds the corners and ids of the charuco board on the image. Adds these to aCornersAll and aIdsAll arrays

        Args:
            aIds (numpy.ndarray): _description_
            aCorners (numpy.ndarray): _description_
            aImageGrayScale (image): _description_
            aCharucoBoard (cv2.aruco.CharucoBoard): _description_
            aCornersAll (list): _description_
            aIdsAll (list): _description_
        """
        if aIds is None:
            # if myIDs doesn't exist, it does this
            print("couldn't detect a charuco board")
        else:
            # if myIDs exist, it does this
            response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(markerCorners=aCorners,
                                                                                     markerIds=aIds,
                                                                                     image=aImageGrayScale,
                                                                                     board=aCharucoBoard,
                                                                                     cameraMatrix=None, 
                                                                                     distCoeffs=None, 
                                                                                     minMarkers=1)
            
            aCornersAll.append(charuco_corners)
            aIdsAll.append(charuco_ids)
            
                     
    def DrawCharuco(aImage, aIds, aCorners):
        """ Draw the detected charuco corners of on the Charuco board image

        Args:
            aImage (_type_): the image of the charuco board to be drawn on
            aIds (_type_): the ids of the aruco markers on the charuco board
            aCorners (_type_): the corners on the charuco board
        """
        aImage = aruco.drawDetectedCornersCharuco(
                image=aImage,
                charucoCorners=aCorners, charucoIds=aIds ) # charucoIds=aIds for displaying ids 
        
        
    def FindIntrinsicAndExtrinsicCoefficients(self, aCornersAll, aIdsAll, aCharucoBoard, aImageSize):
        """finds intrinsic and extrinsix coefficients of a charuco board using the corners and ids detected from the image and save them as variables

        Args:
            aCornersAll (_type_): all corners on a charuco board image
            aIdsAll (_type_):  all ids in a charuco board image
            aCharucoBoard (_type_): the charuco board we are working with
            aImageSize (_type_): size of the image

        Returns:
            _type_: _description_
            returns the tuple (cameraMatrix, distCoeffs, rvecs, tvecs)
            
        """
        calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(charucoCorners=aCornersAll,
                                                                                           charucoIds=aIdsAll,
                                                                                           board=aCharucoBoard,
                                                                                           imageSize=aImageSize,
                                                                                           cameraMatrix=None,
                                                                                           distCoeffs=None)
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs
        self.rvecs = rvecs
        self.tvecs = tvecs
        
        return (cameraMatrix, distCoeffs, rvecs, tvecs)
    
    
    def FindIntrinsicAndExtrinsicCoefficients(self, aCornersAll, aIdsAll, aCharucoBoard, aImageSize):
        """finds intrinsic and extrinsix coefficients of a charuco board using the corners and ids detected from the image

        Args:
            aCornersAll (_type_): all corners on a charuco board image
            aIdsAll (_type_):  all ids in a charuco board image
            aCharucoBoard (_type_): the charuco board we are working with
            aImageSize (_type_): size of the image

        Returns:
            cameraMatrix: camera matrix
            distCoeffs: distortion coefficients
            rvecs: rvecs
            tvecs: tvecs       
        """
        calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(charucoCorners=aCornersAll,
                                                                                           charucoIds=aIdsAll,
                                                                                           board=aCharucoBoard,
                                                                                           imageSize=aImageSize,
                                                                                           cameraMatrix=None,
                                                                                           distCoeffs=None)
        
        return (cameraMatrix, distCoeffs, rvecs, tvecs)
    
    
    def drawFrameAxesOnImage(self, aImage, aCameraMatrix, aDistCoeffs, aRvecs, aTvecs, aLength, aThickness):
        """ draws coordinate axes (x, y and z) on the given image

        Args:
            aImage (_type_): the image you want to draw axes on
            aCameraMatrix (_type_): camera matrix
            aDistCoeffs (_type_): distortion coefficients
            aRvecs (_type_): rvecs
            aTvecs (_type_): tvecs
            aLength (_type_): length of the axes drawn
            aThickness (_type_): thickness of the axes drawn
        Returns:
            aImage: the image with the axes drawn
        """
        cv.drawFrameAxes(image=aImage, cameraMatrix=aCameraMatrix, distCoeffs=aDistCoeffs, rvec=aRvecs[0], tvec=aTvecs[0], length=aLength, thickness=aThickness)
        cv.imshow("result", aImage)
        return aImage
    
    
def TakePicturesWithWebcam(aKey):
    cam = cv.VideoCapture(0)

    cv.namedWindow("video")

    img_counter = 0

    while aKey%256 != 27:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv.imshow("video", frame)

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            return frame
            break
        elif k%256 == 32:
            # SPACE pressed
            img_counter += 1
            return frame
            break

    cam.release()


def main():
    # myImage = cv.imread("images\webcam_calibration\image_3.jpg")
    xNum = 7    # The number of squares in the X direction
    yNum = 5    # The number of squares in the Y direction

    squareSize = 0.02836 # The size of the squares. It is the length of one side
    markerSize = 0.01772 # The size of the aruco markers. It is the length of one side

    myDict = aruco.Dictionary_get(aruco.DICT_7X7_100 ) # The dictionary that we use for the aruco markers my images
    # myDict = aruco.Dictionary_get(aruco.DICT_6X6_1000 ) # The dictionary that we use for the aruco markers for testCase image

    # The gridboard that includes the charuco board information
    myGridBoard = cv.aruco.CharucoBoard.create(xNum, yNum, squareSize, markerSize, myDict)
    
    k = 32 
    while k%256 == 32:
        myImage = TakePicturesWithWebcam(k)
        myCharucoBoard = CharucoBoard(myImage, myDict, myGridBoard)
        cv.imshow("result", myCharucoBoard.image)
        print("\nheyya\n")
        k = cv.waitKey(0)
    

    
if __name__ == "__main__":
    main()
    print("\n\n\nExecution Finished\n\n\n")