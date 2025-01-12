from cameras.OV3660 import OV3660
from utils.fileSystem import FileSystem
from exceptions.cameraException import CameraException

class Camera(FileSystem):
    """
    Class to Handle IR Camera
    """
    def __init__(self):
        super().__init__()
        self.__cameraConfig : dict = self._getConfig()["camera"]

        self.__initCamera()

    def __initCamera(self):
        """
        Method to init camera
        """
        cameraName : str = self.__cameraConfig["camera"]
        if cameraName == "OV3660":
            self.__camera : OV3660 = OV3660()
        else:
            raise CameraException(f"Camera {cameraName} is not defined")

    def captureImage(self) -> tuple:
        """
        Method to capture IR image

        return tuple (resolution, image)
        """
        return (self.__camera.getResolution(), self.__camera.getFrame())