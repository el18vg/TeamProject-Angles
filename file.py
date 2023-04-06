import os
import re

filepathinput = input("Please Enter Where the Videos are: ")
# Specify the path to the directory containing the files
print(filepathinput)

dir_path = "C:/Users/fredg/Desktop/Varun-Videos-Trim"


# Get a list of files in the directory
file_list = os.listdir(dir_path)

# Filter the file list to include only files with names starting with a number
numbered_files = [f for f in file_list if re.match(r"^\d+\.-", f)]

# Print the list of numbered files
print("Numbered files in the directory:")
for f in numbered_files:
    print(f)

# Get user input for the desired number
notnotvalid = 1
while notnotvalid:
    user_input = input("Enter a number between 0 and 21: ")
    if(int(user_input) not in range(1,22)):
        print("not correct")
        notnotvalid = 1
       
    else:
        notnotvalid = 0


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
else:
    print("No file with the desired number exists.")