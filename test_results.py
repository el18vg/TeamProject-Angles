import cv2
import numpy as np
import os
import re
import math

filedir = open("filepath.txt","r")

first_line = filedir.readline()
#print(first_line)

#getting the current directory need this for the textfiles
currentdir = os.getcwd()

# this is location of the folder
dir_path = first_line

os.chdir(dir_path)
# Get a list of files in the directory
file_list = os.listdir(dir_path)

# Filter the file list to include only files with names starting with a number
numbered_files = [f for f in file_list if re.match(r"^\d+\.-", f)]

# sorting the numbered_files out so it can be seen for the user
numbered_files = sorted(numbered_files, key=lambda x: int(x.split('.')[0]))
#print(numbered_files)

# Print the list of numbered files
print("Files in the Directory:")
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
    # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("mask", width, height)
    # cv2.namedWindow("masked_frame", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("masked_frame", width, height)
    # Set the window to full screen mode
    #cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    os.chdir(currentdir)
    filename = "timestamp.csv"
    # checking if file exists
    if os.path.exists(filename):
        #append_write = 'a' # append if already exists
        os.remove(filename)
        
    #else:
        #append_write = 'w' # make a new file if not
    append_write = 'w'
    # open file
    file = open(filename,append_write)

    #writing data to file
    if (append_write == "w"):
        file.write("TimeStamp,FrameCount,Angle\n")

    print("Setup Complete \n")
    return

def writingtofile(timesecond, currentframecount, angles):
    os.chdir(currentdir)
    with open('timestamp.csv', 'a') as timefile:
    #first_line = framefile.readline()
        timefile.write(str(timesecond)+ "," + str(currentframecount) + "," + str(angles) + "\n")
        print("Timestamp:" + str(timesecond)+ ", Current Frame Count:" + str(currentframecount) + ", Angle:" + str(angles))
    return

def defaultvalues():
    # Define the range of red color in HSV
    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])

    # # Apply morphological opening to remove small objects from the foreground
    kernel = np.ones((5,5),np.uint8)
    return lower_white, upper_white, kernel

def sectionchoice(inputvalue, filevalue):
    # for the testing video 6
    if filevalue in [6]:
        black1 = cv2.rectangle(refblack,(400,500),(500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "2"):
                blacksection = cv2.rectangle(blackpoint,(680,50),(850,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
                blacksection = cv2.rectangle(blackpoint,(900,50),(1150,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
                blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    ## for the testing video 7
    elif filevalue in [7, 10, 11, 18, 19, 20, 21]:
        black1 = cv2.rectangle(refblack,(560,500),(670,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "2"):
                blacksection = cv2.rectangle(blackpoint,(830,50),(1000,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
                blacksection = cv2.rectangle(blackpoint,(1050,50),(1300,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
                blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    # for the testign video 12
    elif filevalue in [12, 13, 14, 15]:
        black1 = cv2.rectangle(refblack,(530,500),(640,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "2"):
                blacksection = cv2.rectangle(blackpoint,(790,50),(960,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
                blacksection = cv2.rectangle(blackpoint,(950,50),(1250,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
                blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    # for the testing video 17
    elif filevalue in [16, 17]:
        black1 = cv2.rectangle(refblack,(530,500),(640,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "2"):
                blacksection = cv2.rectangle(blackpoint,(790,50),(960,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
                blacksection = cv2.rectangle(blackpoint,(1000,50),(1250,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
                blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    else:
        black1 = cv2.rectangle(refblack,(430,500),(550,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "2"):
                blacksection = cv2.rectangle(blackpoint,(700,50),(900,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "3"):
                blacksection = cv2.rectangle(blackpoint,(950,50),(1200,1000),(255, 255, 255), -1)   #---the dimension of the ROI
        if(inputvalue == "4"):
                blacksection = cv2.rectangle(blackpoint,(1090,50),(1500,1000),(255, 255, 255), -1)   #---the dimension of the ROI
    return blacksection, black1

# setup the system 
setup()

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(num_frames)


slow_motion_fps = 240
content_duration = 1  # seconds
effective_fps =    slow_motion_fps /content_duration

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()


    #print(len(frame))
    # If the frame was read successfully, display it
    if ret:
        

        # Get the current frame number
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # Calculate real-time millisecond timestamp
        real_time_ms = int((current_frame / effective_fps) * 1000)

        # Print the real-time millisecond timestamp
        #print("Real-time Millisecond Timestamp: ", real_time_ms)

        # holds the ref middlepoint
        refmiddlepoint = []

        # holds the section middlepoint
        sectionmiddlepoint = []

        lower_white, upper_white, kernel = defaultvalues()
        
        ## this is to create a black out
        refblack = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB
        blackpoint = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8) #---black in RGB

        
        blacksection, black1 = sectionchoice(inputvalue, desired_number)

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
        #cv2.imshow("masked_frame", newframe)

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

        # ## angle stuff

        # print("blueline: "+ str(bluelinesize))
        # print("greenline:"+ str(greenlinesize))
        # print("redline: "+ str(redlinesize))
        # #
        if redlinesize > 1:
            angle = math.acos(-(((redlinesize**2) - (bluelinesize**2) - (greenlinesize**2))/(2*bluelinesize*greenlinesize)))
            angleindeg = math.degrees(angle)
            #print("angle: " + str(angleindeg))
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_thickness = 4
            text_color = (0, 0, 0)  # white

            text = "Angle: %.3f Degrees" %angleindeg
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_width, text_height = text_size
            text_x = 10
            text_y = 200
            titletext = "Test: " + str(desired_number) + " Section: " + str(inputvalue)
            text_size, _ = cv2.getTextSize(titletext, font, font_scale, font_thickness)

            cv2.rectangle(frame, (5,20),(730,250),(255, 255, 255), -1)
            cv2.putText(frame, titletext, (text_x, text_y-100), font, font_scale, text_color, font_thickness)

            cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

            writingtofile(real_time_ms, current_frame, angleindeg)
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_thickness = 4
            text_color = (0, 0, 0)  # white
            text = "Angle: 0 Degrees"
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_width, text_height = text_size
            text_x = 10
            text_y = 200
            titletext = "Test: " + str(desired_number) + " Section: " + str(inputvalue)
            text_size, _ = cv2.getTextSize(titletext, font, font_scale, font_thickness)
            angleindeg = 0
            cv2.rectangle(frame, (5,20),(730,250),(255, 255, 255), -1)
            cv2.putText(frame, titletext, (text_x, text_y-100), font, font_scale, text_color, font_thickness)

            cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
            writingtofile(real_time_ms, current_frame, angleindeg)

        # print("")
        # print(overallmidpoint)
        # print(sectionmiddlepoint)
        # print(redlinesize)
        # print("")
        # print(middlepoint)

        # Define the text properties
        

        #cv2.imshow("mask", mask)
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