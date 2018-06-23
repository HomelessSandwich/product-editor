from PIL import Image, ImageOps
from operator import itemgetter

def GetTopPixel(threshold, image, rgbImgWidth, rgbImgHeight, r, g, b):
	topPixel = (0, 0)
	for i in range(rgbImgHeight):
		for j in range(rgbImgWidth):
			currentR, currentG, currentB = image.getpixel((j, i))	
			if ((currentR > (1 + threshold) * r) or (currentR < threshold * r)) and ((currentG > (1 + threshold) * g) or (currentG < threshold * g)) and ((currentB > (1 + threshold) * b) or (currentB < threshold * b)):
				topPixel = (j , i)
				return topPixel

def GetBottomPixel(threshold, image, rgbImgWidth, rgbImgHeight, r, g, b):
	bottomPixel = (0, 0)
	for i in reversed(range(rgbImgHeight)):
		for j in reversed(range(rgbImgWidth)):
			currentR, currentG, currentB = image.getpixel((j, i))		
			if ((currentR > (1 + threshold) * r) or (currentR < threshold * r)) and ((currentG > (1 + threshold) * g) or (currentG < threshold * g)) and ((currentB > (1 + threshold) * b) or (currentB < threshold * b)):
				bottomPixel = (j , i)
				return bottomPixel

def GetLeftPixel(threshold, image, rgbImgWidth, rgbImgHeight, r, g, b):
	leftPixel = (0, 0)
	for i in range(rgbImgWidth):
		for j in range(rgbImgHeight):
			currentR, currentG, currentB = image.getpixel((i, j))		
			if ((currentR > (1 + threshold) * r) or (currentR < threshold * r)) and ((currentG > (1 + threshold) * g) or (currentG < threshold * g)) and ((currentB > (1 + threshold) * b) or (currentB < threshold * b)):
				leftPixel = (i , j)
				return leftPixel
				
def GetRightPixel(threshold, image, rgbImgWidth, rgbImgHeight, r, g, b):
	rightPixel = (0, 0)
	for i in reversed(range(rgbImgWidth)):
		for j in reversed(range(rgbImgHeight)):
			currentR, currentG, currentB = image.getpixel((i, j))		
			if ((currentR > (1 + threshold) * r) or (currentR < threshold * r)) and ((currentG > (1 + threshold) * g) or (currentG < threshold * g)) and ((currentB > (1 + threshold) * b) or (currentB < threshold * b)):
				rightPixel = (i , j)
				return rightPixel

def FindEdges(threshold, image, r, g, b):
	rgbImg = image.convert('RGB')
	rgbImgWidth, rgbImgHeight = rgbImg.size

	topPixel = GetTopPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight, r, g, b)
	bottomPixel = GetBottomPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight, r, g, b)
	leftPixel = GetLeftPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight, r, g, b)
	rightPixel = GetRightPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight, r, g, b)

	return topPixel, bottomPixel, leftPixel, rightPixel

def CropImage(topPixel, bottomPixel, leftPixel, rightPixel, image):
	imageWidth, imageHeight = image.size

	leftPixel = (round(leftPixel[0] - 0.01 * imageWidth), leftPixel[1])
	topPixel = (topPixel[0], round(topPixel[1] - 0.01 * imageHeight))
	rightPixel = (round(rightPixel[0] + 0.01 * imageWidth), rightPixel[1])
	bottomPixel = (bottomPixel[0], round(bottomPixel[1] + 0.01 * imageHeight))
	# Buffers away from the detected edges to avoid small clipping

	image = image.crop((leftPixel[0], topPixel[1], rightPixel[0], bottomPixel[1]))
	#"The crop rectangle, as a (left, upper, right, lower)-tuple."
	return image

def FindBackgroundColour(image):
	imageWidth, imageHeight = image.size
	redPixels = []
	greenPixels = []
	bluePixels = []

	for x in range(imageWidth - 1):
		pixel = image.getpixel((x, 0))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for x in range(imageWidth - 1):
		pixel = image.getpixel((x, imageHeight - 1))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for y in range(imageHeight - 1):
		pixel = image.getpixel((0, y))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for y in range(imageHeight - 1):
		pixel = image.getpixel((imageWidth - 1, y))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])

################################################
# CREATE FUNCTION FOR THIS!!!!! AND FOR FIRST FUNCTIONS!
################################################

	averagePixel = (round(sum(redPixels) / len(redPixels)), round(sum(greenPixels) / len(greenPixels)), round(sum(bluePixels) / len(bluePixels)))
	return averagePixel

def SeperateRGB(colour):
	r = colour[0]
	g = colour[1]
	b = colour[2]
	return r, g, b