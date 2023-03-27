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

# # Apply morphological opening to remove small objects from the foreground
kernel = np.ones((5,5),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# # Find contours in the image
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# convert the object tuple into a string
contourslist  = list(contours)
contourslist.sort(reverse=True, key= cv2.contourArea)

# middle point list
middlepoint = []

#this runs through the top 2 max sizes and then will draw an box around them
for contour in contourslist[0:2]:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 10)
    xvalue = (x+w/2)
    yvalue = (y+h/2)
    print(x, y , w, h)
    print(xvalue, yvalue)
    middlepoint.append([xvalue, yvalue]) 

#print(int(middlepoint[1][0]))
cv2.line(img, (int(middlepoint[0][0]), int(middlepoint[0][1])), (int(middlepoint[1][0]), int(middlepoint[1][1])), (255,0,0), 10)
# Show the image with the green spots identified
width = 1360
height = 1024
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("mask", width, height)
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", width, height)

cv2.imshow('img', img)
#cv2.imshow("mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()