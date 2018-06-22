#
# Oliver Wilkins 21/06/18
# This script downscales an image to 900 x 900 and keeps its aspect ratio, puts a logo in the bottom right hand corner. It then puts this onto a white background.
#

from PIL import Image
from EdgeFind import *
from RuntimeChecks import *

numEdited = 0
threshold = 0.95
workingDirectory = GetWorkingDirectory()
DirectoryCheck(workingDirectory)
inputFiles = GetInputFiles()

if CheckImageExists(workingDirectory + "/logos/logo.png") == True:
	logo = Image.open(workingDirectory + "/logos/logo.png")
	logoWidth, logoHeight = logo.size

backgroundHeight, backgroundWidth = GetUserInputs()


for fileName in inputFiles:
	# Iterates through all the files within the input folder

	if CheckImageExists(workingDirectory + "/input/" + fileName) == True:

		#productCode = GetProductCode(fileName)
		# CheckDirectoryExists(workingDirectory + "/output/" + productCode)
		product = Image.open(workingDirectory + "/input/" + fileName)

		backgroundColour = FindBackgroundColour(product)
		r, g, b = SeperateRGB(backgroundColour)
		background = Image.new('RGB', (backgroundWidth, backgroundHeight), backgroundColour)
		# Creates a solid colour for a background

		topPixel, bottomPixel, leftPixel, rightPixel = FindEdges(threshold, product, r, g, b)

		if topPixel and bottomPixel and leftPixel and rightPixel != (0, 0):
			product = CropImage(topPixel, bottomPixel, leftPixel, rightPixel, product)
			# Crops the image down to the edges of the product

		product.thumbnail((int(backgroundWidth * 0.8), int(backgroundHeight * 0.8)), Image.ANTIALIAS)
		# Scales the image, whilst maintaining the aspect ratio
		# int is used instead of rounding, as it's quicker

		productWidth, productHeight = product.size
		locationX = int(backgroundWidth / 2 - productWidth / 2)
		locationY = int(backgroundHeight / 2 - productHeight / 2)
		# Finds the location on the blank canvas to centre the scaled image

		background.paste(product, (locationX, locationY))
		# Pastes the product onto the white background

		product.close()

		if CheckImageExists(workingDirectory + "/logos/logo.png", debug = False) == True:
			if (logoWidth <= backgroundWidth) and (logoHeight <= backgroundHeight): 
				background.paste(logo, (backgroundWidth - logoWidth, backgroundHeight - logoHeight))
				# Pastes the logo onto the bottom right corner
				# Checks to see if the logo fits onto the background
			else:
				print("Logo does not fit onto background!")

		background.save(workingDirectory + '/output/' + fileName, quality = 100)
		# Saves the image to the output folder
		background.close()

		numEdited += 1
		print(fileName + " has been edited and saved!")
logo.close()

print("\n" + str(numEdited) + " files have been edited and saved!")
# Allows the user to compare the number of edited pictures to the number of files in the input folder
input("Press enter to exit...")