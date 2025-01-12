import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

url : str = "http://192.168.178.58:10900/captureImages"

receivedData : dict = None

try:
    response : requests.models.Response = requests.get(url)
    print(type(response))
    receivedData = response.json()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except ValueError:
    print("Response is not valid JSON")
except Exception as err:
    print(f"An error occurred: {err}")

if receivedData is None:
    raise Exception(f"No response from server {url}")

shapeImage : tuple = tuple(receivedData["image"]["shape"])

image : np.ndarray = np.array(receivedData["image"]["data"]).reshape(shapeImage).astype(np.uint8)

shapeIrImage : tuple = tuple(receivedData["imageIr"]["shape"])

thermalData : np.ndarray = np.array(receivedData["imageIr"]["data"]).reshape(shapeIrImage)

thermalMin = np.min(thermalData)
thermalMax = 45 
normalizedArray = (thermalData - thermalMin) / (thermalMax - thermalMin)

colormap : LinearSegmentedColormap = plt.cm.hot

coloredImage : np.ndarray = (colormap(normalizedArray) * 255).astype(np.uint8)

# Plot both images
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Create two side-by-side plots

# Display the first image
axes[0].imshow(image)
axes[0].axis('off')  # Hide axes
axes[0].set_title('Original Image')

# Display the thermal image
axes[1].imshow(coloredImage)
axes[1].axis('off')  # Hide axes
axes[1].set_title('Thermal Image')

# Show the combined plot
plt.tight_layout()
plt.show()