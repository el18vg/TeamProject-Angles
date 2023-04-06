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


while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was read successfully, display it
    if ret:

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