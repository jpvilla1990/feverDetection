import board
import busio
import adafruit_mlx90640
from cameras.abstractClasses.abstractIRCamera import AbstractIRCamera

class MLX90640(AbstractIRCamera):
    """
    Class to handle MLX90640 IR Camera
    """
    def __init__(self):
        self.__resolution : list = [24,32]
        self.__mlx : adafruit_mlx90640.MLX90640 = adafruit_mlx90640.MLX90640(busio.I2C(board.SCL, board.SDA))
        self.__mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

    def getResolution(self) -> list:
        """
        Method to get camera resolution
        """
        return self.__resolution
    
    def getFrame(self) -> list:
        """
        Method to capture a frame
        """
        frame : list = [0] * (self.__resolution[0] * self.__resolution[1])
        self.__mlx.getFrame(frame)
        return frame