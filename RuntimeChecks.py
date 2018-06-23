import os
from PIL import Image

def GetWorkingDirectory():
	return os.path.dirname(os.path.abspath(__file__))
	# Gets the working directory - avoids any issues that may occur

def CheckDirectoryExists(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)

def DirectoryCheck(directory):
	here = GetWorkingDirectory()
	CheckDirectoryExists(here + "/input")
	CheckDirectoryExists(here + "/output")
	# Checks to see if there is an input and output, if not, it creates them

def GetInputFiles():
	return os.listdir(GetWorkingDirectory() + "/input")

def GetUserInputs():
	while True:
		try:
			backgroundHeight = int(input("\nPlease enter the height (in pixels) for your edited images: "))
			if backgroundHeight > 10000 or backgroundHeight < 1:
				raise ValueError
			backgroundWidth = int(input("Please enter the width (in pixels) for your edited images: "))
			# Asks the user for the height and width (in pixels) 
			if backgroundWidth > 10000 or backgroundWidth < 1:
				raise ValueError
			break
		except ValueError:
			print("\nOops! That was not a valid number. Try again...")
			# Throws an error if the user did not enter an integer
	return backgroundHeight, backgroundWidth

def GetProductCode(fileName):
	return (fileName.split("-"))[0]

def CheckImageExists(directory, debug = True):
		if os.path.exists(directory) and (directory.endswith(".jpg") or directory.endswith(".jpeg") or directory.endswith(".png")):
			return True
		else:
			if debug == True:
				print(directory + " cannot be found or the image is not in the JPEG or PNG format!")
			return False
