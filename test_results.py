import cv2
import numpy as np
import os
import re
import math

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
print("")
# Get user input for the desired number
notnotvalid = 1
while notnotvalid:
    user_input = input("Enter The Testing Video Number between 0 and 21: ")
    if(int(user_input) not in range(1,22) or int(user_input) == 8):
        print("This is not correct or Does not exist")
        notnotvalid = 1
    else:
        print("")
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
    print("Testing File Selected:", matching_file)
    print("")
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

def setup():
    width = 1920
    height = 1080
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", width, height)
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("mask", width, height)
    cv2.namedWindow("masked_frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("masked_frame", width, height)

    
    print("Setup Complete \n")
    return


def defaultvalues():
    # Define the range of red color in HSV
    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])

    # # Apply morphological opening to remove small objects from the foreground
    kernel = np.ones((5,5),np.uint8)
    return lower_white, upper_white, kernel

def sectionchoice(inputvalue):
    if(inputvalue == "2"):
            blacksection = cv2.rectangle(blackpoint,(700,50),(900,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    if(inputvalue == "3"):
            blacksection = cv2.rectangle(blackpoint,(950,50),(1200,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    if(inputvalue == "4"):
            blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    return blacksection



setup()

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was read successfully, display it
    if ret:
        # holds the ref middlepoint
        refmiddlepoint = []

        # holds the section middlepoint
        sectionmiddlepoint = []

        lower_white, upper_white, kernel = defaultvalues()
        
        ## this is to create a black out
        refblack = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB
        blackpoint = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB

        black1 = cv2.rectangle(refblack,(430,500),(550,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        
        blacksection = sectionchoice(inputvalue)

        # for the reference
        gray = cv2.cvtColor(refblack,cv2.COLOR_BGR2GRAY)               #---converting to gray
        retnew, b_mask = cv2.threshold(gray,127,255, 0)                 #---converting to binary image

        masked_frame = cv2.bitwise_and(frame,frame,mask = b_mask)

        rgb = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

        # Threshold the rgb image to get only red colors
        refmask = cv2.inRange(rgb, lower_white, upper_white)
        
        refmask = cv2.morphologyEx(refmask, cv2.MORPH_OPEN, kernel)      

        # # Find contours in the image
        refcontours, hierarchy = cv2.findContours(refmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # convert the object tuple into a string
        refcontourslist  = list(refcontours)
        refcontourslist.sort(reverse=True, key= cv2.contourArea)
        #print(refcontourslist)

        if(len(refcontourslist) > 0):
            for contour in refcontourslist[0:1]:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 10)
                ## this holds the middle point per frame
                refxvalue = (x+w/2)
                refyvalue = (y+h/2)
                refmiddlepoint.append([refxvalue, refyvalue]) 
                if (len(overallmidpoint) <= 2):
                    overallmidpoint.append([refxvalue, refyvalue])
        #####################################################################################################

        # for the section
        gray2 = cv2.cvtColor(blackpoint,cv2.COLOR_BGR2GRAY)               #---converting to gray
        retnew, b_mask2 = cv2.threshold(gray2,127,255, 0)                 #---converting to binary image

        masked_frame2 = cv2.bitwise_and(frame,frame,mask = b_mask2)

        rgb2 = cv2.cvtColor(masked_frame2, cv2.COLOR_BGR2RGB)

        # Threshold the rgb image to get only red colors
        sectionmask = cv2.inRange(rgb2, lower_white, upper_white)

        # # Apply morphological opening to remove small objects from the foreground
        sectionmask = cv2.morphologyEx(sectionmask, cv2.MORPH_OPEN, kernel)      

        # # Find contours in the image
        sectioncontours, hierarchy = cv2.findContours(sectionmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # convert the object tuple into a string
        sectioncontourslist  = list(sectioncontours)
        sectioncontourslist.sort(reverse=True, key= cv2.contourArea)

        if(len(sectioncontourslist) > 0):
            for contour in sectioncontourslist[0:1]:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 10)
                ## this holds the middle point per frame
                sectionxvalue = (x+w/2)
                sectionyvalue = (y+h/2)
                sectionmiddlepoint.append([sectionxvalue, sectionyvalue]) 
                if (len(overallmidpoint) <=2):
                    overallmidpoint.append([sectionxvalue, sectionyvalue])

        #####################################################################################

        newframe = cv2.bitwise_or(masked_frame, masked_frame2)
        cv2.imshow("masked_frame", newframe)

        mask = cv2.bitwise_or(refmask,sectionmask)

        # # green line
        cv2.line(frame, (int(overallmidpoint[0][0]), int(overallmidpoint[0][1])), (int(overallmidpoint[1][0]), int(overallmidpoint[1][1])), (0,255,0), 4)
        
        greenlinesize = math.sqrt((overallmidpoint[1][0]-overallmidpoint[0][0])**2 + (overallmidpoint[1][1] - overallmidpoint[0][1])**2)
        
        #print(overallmidpoint)
        #print(greenlinesize)
        
        # # blue line
        cv2.line(frame, (int(refmiddlepoint[0][0]), int(refmiddlepoint[0][1])), (int(sectionmiddlepoint[0][0]), int(sectionmiddlepoint[0][1])), (255,0,0), 10)

        bluelinesize = math.sqrt((sectionmiddlepoint[0][0]-refmiddlepoint[0][0])**2 + (sectionmiddlepoint[0][1] - refmiddlepoint[0][1]) **2)

        ## red line
        cv2.line(frame, (int(overallmidpoint[1][0]),int(overallmidpoint[1][1])), (int(sectionmiddlepoint[0][0]),int(sectionmiddlepoint[0][1])), (0,0,255), 5)

        redlinesize = math.sqrt((overallmidpoint[1][0] - sectionmiddlepoint[0][0])**2 + (overallmidpoint[1][1] - sectionmiddlepoint[0][1])**2)

        ## angle stuff

        print("blueline: "+ str(bluelinesize))
        print("greenline:"+ str(greenlinesize))
        print("redline: "+ str(redlinesize))
        #
        if redlinesize > 1:
            angle = math.acos(-(((redlinesize**2) - (bluelinesize**2) - (greenlinesize**2))/(2*bluelinesize*greenlinesize)))
            angleindeg = math.degrees(angle)
            print("angle: " + str(angleindeg))
        #print("")
        # print(overallmidpoint)
        # print(sectionmiddlepoint)
        # print(redlinesize)
        # print("")
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