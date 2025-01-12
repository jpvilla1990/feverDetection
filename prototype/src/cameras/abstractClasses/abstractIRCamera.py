from abc import ABC, abstractmethod

class AbstractIRCamera(ABC):
    """
    Abstract class for IR cameras
    """
    @abstractmethod
    def getResolution(self) -> list:
        """
        Method to get resolution in form of a list
        """
        pass

    @abstractmethod
    def getFrame(self) -> list:
        """
        Method to get frame in form of a list already serialized
        """
        pass