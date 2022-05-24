# Continous Acquisition
# This code makes an automatic acquisition of the first Vimba GigE camera on subnet
# and record it with current storage ring current and mirror temperature as filename
# It also creates a .txt files with current, temperatures, preassure and date time information
# All data is stored in a folder created in the same path as this .py file.
# Every time this .py file is runned a folder is created with date time name.

# Authors: Thiago Santos (miguel.thiagos@gmail.com), The Imbuia Group, February 2022



#Libraries needed
import threading
import sys
import cv2
from datetime import datetime
import os
import time
import matplotlib.pyplot as plt
from epics import caget
from typing import Optional
from vimba import *

#Getting date and time information individuously

now = datetime.now()

year = now.strftime("%Y")
print(year)
month = now.strftime("%m")
print(month)
day = now.strftime("%d")
print(day)
hour = now.strftime("%H")
print(hour)
minute = now.strftime("%M")
print(minute)
second = now.strftime("%S")
print(second)

#Creating date and time variables: Note time_data is the information, time is a function from time library.
date = day+"/"+month+"/"+year
time_data = hour+":"+minute+":"+second


#Creating the filename for .txt log file
filename = "imbuia_log_"+day+"-"+month+"-"+year+"_"+hour+"-"+minute+"-"+second+".txt"

# Creating a subfolder and log file for PVs values

#Name for new folder
foldername = day+"-"+month+"-"+year+"_"+hour+"-"+minute+"-"+second

#Getting current directory
directory = os.path.dirname(os.path.abspath(__file__))

#Joining current directory and new folder name
path = os.path.join(directory, foldername)

#Creating new folder with all permissions
os.mkdir(path,0o777)

# Log file name with path
filename = path+"/"+filename

#Creating .txt file and writing head information
file = open(filename,"w+")
file.write("Log file for beam diagnostics\nImbuia Beamline\n\ndate;time;current;Temperature 1;Temperature 2;P1;P2;P3;P4;image name")
file.close()

print("Created log file: "+filename)
time.sleep(5)


#Infinite loop start
while 1==1:

	#Take current time date

	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%m")
	day = now.strftime("%d")
	hour = now.strftime("%H")
	minute = now.strftime("%M")
	second = now.strftime("%S")

	# Take current current

	mA = caget("SI-Glob:AP-CurrInfo:Current-Mon")
	mA = str(mA)

	print("Current value = "+ mA +" mA")

	# Take current temperatures

	temp1 = caget("IMB:F:EPS01:MR1TT1")
	temp1 = str(temp1)

	temp2 = caget("IMB:F:EPS01:MR1TT2")
	temp2 = str(temp2)

	print("Current temperature = \n"+ temp1 + " °C\n" + temp2+" °C")


	# Take current preassures

	p1 = caget("SI-07C2:VA-SIP20-BG:Pressure-Mon")
	p1 = str(p1)

	p2 = caget("SI-07SPFE:VA-CCG-MD:Pressure-Mon")
	p2 = str(p2)

	p3 = caget("SI-07C1:VA-CCG-BG:Pressure-Mon")
	p3 = str(p3)

	p4 = caget("SI-07C3:VA-CCG-BG:Pressure-Mon")
	p4 = str(p4)

	print("Preassure values = \n"+ p1 +" \n"+p2+"\n"+p3+"\n"+p4+"\n")


	# Image filename composition

	img_name = "imbuia_"+day+month+year+"_"+hour+minute+second+".jpg"
	img_name_path = path +"/"+ img_name

	# Appending information to .txt log file

	file = open(filename,"a")
	file.write("\n"+date+";"+time_data+";"+mA+";"+temp1+";"+temp2+";"+p1+";"+p2+";"+p3+";"+p4+";"+img_name)
	file.close()

	# Acquiring and saving image

	with Vimba.get_instance() as vimba :
		cams = vimba.get_all_cameras()
		with cams [0] as cam:
			frame = cam.get_frame()
			frame.convert_pixel_format (PixelFormat.Mono8)
			cv2.imwrite (img_name_path, frame.as_opencv_image())
			print('Image acquired: '+img_name+' \n')

	# Sleep time
	print ('Waiting for next acquisition\n')
	time.sleep(3)
