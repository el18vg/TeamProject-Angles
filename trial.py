import cv2
import numpy as np

# Load the image
img = cv2.imread('image2.jpg')

# Define the box region
#x, y, w, h = 400, 400, 1000, 1000

# Create a white mask of the same size as the image
black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB

black1 = cv2.rectangle(black,(700,600),(3800,1400),(255, 255, 255), -1)   #---the dimension of the ROI
gray = cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)               #---converting to gray
ret,b_mask = cv2.threshold(gray,127,255, 0)                 #---converting to binary image

masked_img = cv2.bitwise_and(img,img,mask = b_mask)


#convert space
rgb = cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB)

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
cv2.line(masked_img, (int(middlepoint[0][0]), int(middlepoint[0][1])), (int(middlepoint[1][0]), int(middlepoint[1][1])), (255,0,0), 10)
# Show the image with the green spots identified

width = 1360
height = 1024
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", width, height)
# Display the result
cv2.imshow('image', masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()