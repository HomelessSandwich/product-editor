#
# Oliver Wilkins 21/06/18
# This script downscales an image to 900 x 900 and keeps its aspect ratio, puts a logo in the bottom right hand corner. It then puts this onto a white background.
#

from PIL import Image
from EdgeFind import *
from RuntimeChecks import *

numEdited = 0
workingDirectory = GetWorkingDirectory()
DirectoryCheck(workingDirectory)
inputFiles = GetInputFiles()

if CheckImageExists(workingDirectory + "/logos/logo.png") == True:
	logo = Image.open(workingDirectory + "/logos/logo.png")
	logoWidth, logoHeight = logo.size

backgroundHeight, backgroundWidth, threshold = GetUserInputs()


for fileName in inputFiles:
	# Iterates through all the files within the input folder

	if CheckImageExists(workingDirectory + "/input/" + fileName) == True:

		product = Image.open(workingDirectory + "/input/" + fileName)
		productWidth, productHeight = product.size

		backgroundColour = GetBackgroundColour(product)
		r, g, b = SeperateRGB(backgroundColour)

		topPixel, bottomPixel, leftPixel, rightPixel = FindEdges(threshold, product, r, g, b)

		if topPixel and bottomPixel and leftPixel and rightPixel != (0, 0):
			product = CropImage(topPixel, bottomPixel, leftPixel, rightPixel, product)
			# Crops the image down to the edges of the product

		scaledImage = ScaleImage(product, backgroundWidth, backgroundHeight)

		blendedImage = BlendBackgrounds(scaledImage, backgroundWidth, backgroundHeight)

		if CheckImageExists(workingDirectory + "/logos/logo.png", debug = False) == True:
			if (logoWidth <= backgroundWidth) and (logoHeight <= backgroundHeight): 
				blendedImage.paste(logo, ((backgroundWidth - 1) - (logoWidth - 1) - 1, (backgroundHeight - 1) - (logoHeight - 1) - 1))
				# Pastes the logo onto the bottom right corner
				# Checks to see if the logo fits onto the background
			else:
				print("Logo does not fit onto background!")

		blendedImage.save(workingDirectory + '/output/' + fileName, quality = 100)
		# Saves the image to the output folder

		numEdited += 1
		print(fileName + " has been edited and saved!")
logo.close()

print("\n" + str(numEdited) + " files have been edited and saved!")
# Allows the user to compare the number of edited pictures to the number of files in the input folder
input("Press enter to exit...")