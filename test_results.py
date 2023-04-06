import cv2
import numpy as np
import os
import re

# this is location of the folder
dir_path = "C:/Users/fredg/Desktop/Varun-Videos-Trim"

os.chdir(dir_path)
# Get a list of files in the directory
file_list = os.listdir(dir_path)

# Filter the file list to include only files with names starting with a number
numbered_files = [f for f in file_list if re.match(r"^\d+\.-", f)]

# sorting the numbered_files out so it can be seen for the user
numbered_files = sorted(numbered_files, key=lambda x: int(x.split('.')[0]))
#print(numbered_files)

# Print the list of numbered files
print("Files in the directory:")
for f in numbered_files:
    print(f)
print("\n")
# Get user input for the desired number
notnotvalid = 1
while notnotvalid:
    user_input = input("Enter The Testing Video Number between 0 and 21: ")
    if(int(user_input) not in range(1,22) or int(user_input) == 8):
        print("This is not correct or Does not exist")
        notnotvalid = 1
    else:
        print("\n")
        notnotvalid = 0

# convert the number to int
desired_number = int(user_input)

# Check if a file with the desired number exists in the directory
matching_file = None
for f in numbered_files:
    file_number = int(re.search(r"^(\d+)\.-", f).group(1))
    if file_number == desired_number:
        matching_file = f
        break

if matching_file:
    print("File with desired number:", matching_file)
    print("\n")
else:
    print("No file with the desired number exists.")

# open the video
cap = cv2.VideoCapture(matching_file)

# Check if video is opened successfully
if not cap.isOpened():
    print("Error opening video file")

## set a flag
notvalid = 1

# wait for the flag to be set false
# this check is to make sure that the person has entered a proper section
while notvalid:
    inputvalue = input("Enter what section compared: ")
    if inputvalue not in ['2','3','4']:
        print("not valid input")
        notvalid = 1
    else:
        notvalid = 0

## this holds the first position of the sections measured
overallmidpoint = []

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was read successfully, display it
    if ret:
        width = 1920
        height = 1080
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame", width, height)
        # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("mask", width, height)
        cv2.namedWindow("masked_frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("masked_frame", width, height)

        ## this is to create a black out
        black = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB

        black1 = cv2.rectangle(black,(430,500),(550,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        
        if(inputvalue == "2"):
            black2 = cv2.rectangle(black,(700,50),(900,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
            black3 = cv2.rectangle(black,(950,50),(1200,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
            black4 = cv2.rectangle(black,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI

        gray = cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)               #---converting to gray
        retnew, b_mask = cv2.threshold(gray,127,255, 0)                 #---converting to binary image

        masked_frame = cv2.bitwise_and(frame,frame,mask = b_mask)

        cv2.imshow("masked_frame", masked_frame)

        rgb = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

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

        ## this holds the middle point per frame
        middlepoint = []

        if(len(contourslist) > 1):
            for contour in contourslist[0:2]:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 10)
                xvalue = (x+w/2)
                yvalue = (y+h/2)
                #print(x, y , w, h)
                #print(xvalue, yvalue)
                #print("\n")
                middlepoint.append([xvalue, yvalue]) 
                #if(len(overallmidpoint) <= 2 and (xvalue <= 520) and (xvalue >= 450) and (yvalue <= 700) and (yvalue >= 600)):
                #     overallmidpoint.append([xvalue, yvalue])
                if(len(overallmidpoint) <= 2):
                     overallmidpoint.append([xvalue, yvalue])
        else:     
            continue
        
        # green line
        cv2.line(frame, (int(overallmidpoint[0][0]), int(overallmidpoint[0][1])), (int(overallmidpoint[1][0]), int(overallmidpoint[1][1])), (0,255,0), 4)
        # blue line
        cv2.line(frame, (int(middlepoint[0][0]), int(middlepoint[0][1])), (int(middlepoint[1][0]), int(middlepoint[1][1])), (255,0,0), 10)

        #print(middlepoint)
        cv2.imshow("mask", mask)
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