from cameras.MLX90640 import MLX90640
from utils.fileSystem import FileSystem
from exceptions.cameraException import CameraException

class IrCamera(FileSystem):
    """
    Class to Handle IR Camera
    """
    def __init__(self):
        super().__init__()
        self.__irCameraConfig : dict = self._getConfig()["irCamera"]

        self.__initCamera()

    def __initCamera(self):
        """
        Method to init camera
        """
        cameraName : str = self.__irCameraConfig["camera"]
        if cameraName == "MLX90640-D110":
            self.__camera : MLX90640 = MLX90640()
        else:
            raise CameraException(f"Camera {cameraName} is not defined")

    def captureImage(self) -> tuple:
        """
        Method to capture IR image

        return tuple (resolution, image)
        """
        return (self.__camera.getResolution(), self.__camera.getFrame())