import cv2
import numpy as np


#video title
videotitle = "1.-1metre-Lightweight-trim"

# Create a VideoCapture object
cap = cv2.VideoCapture("C:/Users/USER/OneDrive - University of Leeds/Year 4/MECH5080M -Team Project/Testing/Varun-Videos-Trim/"+videotitle+".mp4")

# Check if video is opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Specify the window size
width = 1920
height = 1080


overallmidpoint = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was read successfully, display it
    if ret:


        

        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #this is the image in grey format
        cv2.imshow("Gray", rgb)

        # Define the range of red color in HSV
        lower_white = np.array([230, 230, 230])
        upper_white = np.array([255, 255, 255])

        # Threshold the rgb image to get only red colors
        mask = cv2.inRange(rgb, lower_white, upper_white)

        # # Apply morphological opening to remove small objects from the foreground
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)      

        # # Find contours in the image
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # convert the object tuple into a string
        contourslist  = list(contours)
        contourslist.sort(reverse=True, key= cv2.contourArea)

        #print(contourslist)
    
        middlepoint = []

        if(len(contourslist) > 1):
            for contour in contourslist[0:4]:
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