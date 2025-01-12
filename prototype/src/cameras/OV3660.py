import cv2
from cameras.abstractClasses.abstractCamera import AbstractCamera

class OV3660(AbstractCamera):
    """
    Class to handle OV3660 IR Camera
    """
    def __init__(self):
        self.__resolution : list = [480,640,3]

    def getResolution(self) -> list:
        """
        Method to get camera resolution
        """
        return self.__resolution
    
    def getFrame(self) -> list:
        """
        Method to capture a frame
        """
        frameList : list = [0] * (self.__resolution[0] * self.__resolution[1] * self.__resolution[2])
        cap : cv2.VideoCapture = cv2.VideoCapture(0)

        if cap.isOpened():
            cap.grab()
            ret, frame = cap.read()

            if not ret:
                return frameList

            frameList = frame[:,::-1,:].reshape(self.__resolution[0] * self.__resolution[1] * self.__resolution[2]).tolist()

        cap.release()

        return frameList