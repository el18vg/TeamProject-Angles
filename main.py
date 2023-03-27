import cv2
import numpy as np

#reading image
img = cv2.imread("image2.jpg")

#convert space
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Resize the image to a smaller size
#img = cv2.resize(img, None, fx=0.2, fy=0.2)


# Define the range of green color in RBG
lower_green = np.array([10, 80, 80])
upper_green = np.array([80, 255, 180])

# Threshold the image to get only green colors
mask = cv2.inRange(rgb, lower_green, upper_green)
