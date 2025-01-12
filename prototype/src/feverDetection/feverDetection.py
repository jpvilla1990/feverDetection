import os
import requests
import numpy as np
import cv2
from ultralytics import YOLO
from utils.fileSystem import FileSystem

class FeverDetection(FileSystem):
    """
    Class to manage data processing
    """
    def __init__(self):
        super().__init__()
        modelName : str = self._getConfig()["yolo"]["model"].split("/")[-1]
        self.__modelPath : str = os.path.join(self._getPaths()["yoloData"], modelName)
        self.__downloadModel()
        self.__model : YOLO = YOLO(
            self.__modelPath,
        )
        self.__desiredConfidence : float = self._getConfig()["yolo"]["desiredConfidence"]
        self.__classDetected : int = self._getConfig()["yolo"]["classDetected"]

    def __downloadModel(self):
        """
        Method to download model
        """
        if not self._checkFileExists(self.__modelPath):
            with requests.get(self._getConfig()["yolo"]["model"], stream=True) as r:
                r.raise_for_status()
                with open(self.__modelPath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)

    def getCoordinatesFace(self, image : tuple) -> list:
        """
        Get coordinates using YOLO
        """
        i : int = 1
        relativeCoordinates : list = []
        results : list = self.__model.predict(source=np.array(image[1]).reshape(tuple(image[0])).astype(np.uint8), save=False, show=False, conf=self.__desiredConfidence)

        for detection in results[0].boxes:
            if detection.cls == self.__classDetected and detection.conf > self.__desiredConfidence:
                x_min, y_min, x_max, y_max = map(int, detection.xyxy[0])

                relativeCoordinates.append(
                    {
                        "xMin" : x_min,
                        "yMin" : y_min,
                        "xMax" : x_max,
                        "yMax" : y_max,
                    }
                )
                #cropped_image : Image.Image = image.crop((x_min, y_min, x_max, y_max))
                #cropped_image.save(f"detected_object_{i}.jpg")
                i += 1

        if len(relativeCoordinates) == 0:
            relativeCoordinates = [[]]

        return relativeCoordinates
