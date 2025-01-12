from PIL import Image
import torch
import numpy

imagePath : str = "Chips_Thermal_Face_Dataset/images/1_37.jpeg"

image : Image.Image = Image.open(imagePath)
imageArray : numpy.ndarray = numpy.array(image).astype(numpy.float32)

intensityArray : numpy.ndarray = imageArray[:,:,0] + imageArray[:,:,1] + imageArray[:,:,2]

maxValue : int = 255 * 3
minTemperature : int = 25.0
maxTemperature : int = 37.5
scale : int = maxTemperature - minTemperature

scaledArray : numpy.ndarray = (((intensityArray / maxValue) * scale) + minTemperature).astype(numpy.uint8)

#image = Image.fromarray(scaledArray, mode='L')

# Save the image as a JPG file
#image.save('single_channel_image.jpg')

temperature : float = scaledArray.max()
print(temperature)