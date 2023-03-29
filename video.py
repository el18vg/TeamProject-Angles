import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture("video2.mp4")

# Check if video is opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Specify the window size
width = 1920
height = 1080
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", width, height)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("mask", width, height)
cv2.namedWindow("masked_frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("masked_frame", width, height)
cv2.namedWindow("new_frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("new_frame", width, height)

overallmidpoint = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was read successfully, display it
    if ret:
        cv2.imshow("new_frame", frame)
        # Create a white mask of the same size as the image
        black = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB

        black1 = cv2.rectangle(black,(380,300),(1000,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        gray = cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)               #---converting to gray
        retnew, b_mask = cv2.threshold(gray,127,255, 0)                 #---converting to binary image

        masked_frame = cv2.bitwise_and(frame,frame,mask = b_mask)

        cv2.imshow("masked_frame", masked_frame)


        # Convert the frame to HSV color space
        rgb = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

        # Define the range of red color in HSV
        lower_red = np.array([15, 30, 25])
        upper_red = np.array([28, 56, 55])

         # Threshold the rgb image to get only red colors
        mask = cv2.inRange(rgb, lower_red, upper_red)

        # # Apply morphological opening to remove small objects from the foreground
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)            

        cv2.imshow("mask", mask)

        # # Find contours in the image
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # convert the object tuple into a string
        contourslist  = list(contours)
        contourslist.sort(reverse=True, key= cv2.contourArea)

        # middle point list
        middlepoint = []
        #print(len(contourslist))
        #this runs through the top 2 max sizes and then will draw an box around them
        if(len(contourslist) > 1):
            for contour in contourslist[0:2]:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 10)
                xvalue = (x+w/2)
                yvalue = (y+h/2)
                print(x, y , w, h)
                print(xvalue, yvalue)
                middlepoint.append([xvalue, yvalue]) 
                if(len(overallmidpoint) <= 2):
                     overallmidpoint.append([xvalue, yvalue])
        else:
            continue
        #print(int(middlepoint[1][0]))
        
        #print(overallmidpoint)
        #print("overallmidpoint", overallmidpoint[0][0], overallmidpoint[0][1], overallmidpoint[1][0], overallmidpoint[1][1] )
        ##green line
        newx = cv2.line(frame, (int(middlepoint[0][0]), int(middlepoint[0][1])), (int(overallmidpoint[1][0]), int(overallmidpoint[1][1])), (0,255,0), 4)
        #print(newx)
        ##blue line
        cv2.line(frame, (int(middlepoint[0][0]), int(middlepoint[0][1])), (int(middlepoint[1][0]), int(middlepoint[1][1])), (255,0,0), 10)

        angle = np.arctan(h/w)
        degrees = np.rad2deg(angle)


        cv2.imshow("Frame", frame)


        # Wait for a key press and exit if 'q' is pressed
        key = cv2.waitKey(0)
        if key & 0xFF == ord('q'):
            break
    else:
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
