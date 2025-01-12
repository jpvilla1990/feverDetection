import time
from fastapi import FastAPI
import uvicorn
from cameras.irCamera import IrCamera
from cameras.camera import Camera
from feverDetection.feverDetection import FeverDetection
from utils.fileSystem import FileSystem

class Server(FileSystem):
    """
    Main class
    """
    def __init__(self):
        super().__init__()
        self.__irCamera : IrCamera = IrCamera()
        self.__camera : Camera = Camera()
        self.__feverDetection : FeverDetection = FeverDetection()

    def getAddress(self) -> dict:
        """
        Method to get address (host and port)
        """
        return {
            "host" : self._getConfig()["server"]["hostIp"],
            "port" : self._getConfig()["server"]["port"]
        }

    def captureImages(self) -> tuple:
        """
        Method to capture Images
        """
        delayCaptureMiliSecondsCamera : float = self._getConfig()["camera"]["delayCaptureMiliSeconds"]
        delayCaptureMiliSecondsIrCamera : float = self._getConfig()["irCamera"]["delayCaptureMiliSeconds"]

        time.sleep(delayCaptureMiliSecondsCamera)
        image : tuple = self.__camera.captureImage()

        detection : list = self.__feverDetection.getCoordinatesFace(image)

        time.sleep(delayCaptureMiliSecondsIrCamera)
        imageIr : tuple = self.__irCamera.captureImage()

        return image + imageIr + tuple(detection)

app : FastAPI = FastAPI()
server : Server = Server()

@app.get("/captureImages")
async def captureImages():
    """
    Endpoint to captureImages GET request.
    """
    images : tuple = server.captureImages()
    return {
        "image" : {
            "shape" : images[0],
            "data" : images[1],
        },
        "imageIr" : {
            "shape" : images[2],
            "data" : images[3],
        },
        "detectedFace" : {
            "data" : images[4],
        }
    }

if __name__ == "__main__":
    address : dict = server.getAddress()
    uvicorn.run(app, host=address["host"], port=address["port"])