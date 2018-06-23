from PIL import Image
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
	leftPixel, topPixel, rightPixel, bottomPixel = GetBufferPixels(topPixel, bottomPixel, leftPixel, rightPixel, image)
	image = image.crop((leftPixel[0], topPixel[1], rightPixel[0], bottomPixel[1]))
	#"The crop rectangle, as a (left, upper, right, lower)-tuple."
	return image


def GetBackgroundColour(image):
	redPixels, greenPixels, bluePixels = GetBorderPixels(image)
	averagePixel = (round(sum(redPixels) / len(redPixels)), round(sum(greenPixels) / len(greenPixels)), round(sum(bluePixels) / len(bluePixels)))
	return averagePixel


def GetBorderPixels(image):
	imageWidth, imageHeight = image.size
	redPixels = []
	greenPixels = []
	bluePixels = []

	for x in range(imageWidth ):
		pixel = image.getpixel((x, 0))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for x in range(imageWidth):
		pixel = image.getpixel((x, imageHeight - 1))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for y in range(imageHeight):
		pixel = image.getpixel((0, y))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	for y in range(imageHeight):
		pixel = image.getpixel((imageWidth - 1, y))	
		redPixels.append(pixel[0])
		greenPixels.append(pixel[1])
		bluePixels.append(pixel[2])
	return redPixels, greenPixels, bluePixels


def GetBufferPixels(topPixel, bottomPixel, leftPixel, rightPixel, image):
	imageWidth, imageHeight = image.size
	borderPercentage = 0.03

	if leftPixel[0] - round(borderPercentage * imageWidth) >= 0:
		leftPixel = (leftPixel[0] - round(borderPercentage * imageWidth), leftPixel[1])
	else:
		leftPixel = (0, leftPixel[1])
	if topPixel[1] - round(borderPercentage * imageHeight) >= 0:
		topPixel = (topPixel[0], topPixel[1] - round(borderPercentage * imageHeight))
	else:
		topPixel = (topPixel[0], 0)
	if rightPixel[0] + round(borderPercentage * imageWidth) <= imageWidth:
		rightPixel = (rightPixel[0] + round(borderPercentage * imageWidth), rightPixel[1])
	else:
		rightPixel = (imageWidth, rightPixel[1])
	if bottomPixel[1] + round(borderPercentage * imageWidth) <= imageHeight:
		bottomPixel = (bottomPixel[0], bottomPixel[1] + round(borderPercentage * imageHeight))
	else:
		bottomPixel = (bottomPixel[0], imageHeight)
	# Buffers away from the detected edges to avoid small clipping
	return leftPixel, topPixel, rightPixel, bottomPixel

	
def SeperateBorders(imageWidth, imageHeight, borderPixels):
	topPixels = borderPixels[0:imageWidth]
	bottomPixels = borderPixels[imageWidth:2*imageWidth]
	leftPixels = borderPixels[2*imageWidth:2*imageWidth + imageHeight]
	rightPixels = borderPixels[2*imageWidth + imageHeight:len(borderPixels)]
	return topPixels, bottomPixels, leftPixels, rightPixels


def SeperateRGB(colour):
	r = colour[0]
	g = colour[1]
	b = colour[2]
	return r, g, b


def CombineRGB(redPixels, greenPixels, bluePixels):
	pixels = []
	for i in range(len(redPixels)):
		pixels.append((redPixels[i], greenPixels[i], bluePixels[i]))
	return pixels


def ScaleImage(image, inputWidth, inputHeight):
		imageWidth, imageHeight = image.size		

		if imageHeight > imageWidth:
			ratio = inputHeight / imageHeight
			scaledHeight = inputHeight
			scaledWidth = imageWidth * ratio
		elif imageWidth > imageHeight:
			ratio = inputWidth / imageWidth
			scaledHeight = imageHeight * ratio
			scaledWidth = inputWidth
		else:
			scaledHeight = inputHeight
			scaledWidth = inputWidth

		return image.resize((round(scaledWidth * 0.8), round(scaledHeight * 0.8)), Image.LANCZOS)
		# 0.8 multiplier to make sure there is a border between the image and the background		
		# Scales the image, whilst maintaining the aspect ratio

		
def CentreImage(image, image2):
	locationX = int(image.width / 2 - image2.width / 2)
	locationY = int(image.height / 2 - image2.height / 2)
	# Finds the location on image for image2 to be centred
	image.paste(image2, (locationX, locationY))
	return image


def BlendBackgrounds(image, backgroundWidth, backgroundHeight):
	image = image.convert('RGB')
	imageWidth, imageHeight = image.size
	print(imageWidth)

	blendLength = round((backgroundWidth - imageWidth) / 2)

	borderedImage = CentreImage(Image.new('RGB', (imageWidth + blendLength * 2 + 1, imageHeight + blendLength * 2 + 1)), image)

	for x in range(imageWidth):
		pixel = image.getpixel((x, 0))
		borderedImage.paste(Image.new('RGB', (1, blendLength), pixel), (blendLength + x, 0)) 
		# Top fill

		pixel = image.getpixel((x, imageHeight - 1))	
		borderedImage.paste(Image.new('RGB', (1, blendLength), pixel), (blendLength + x, imageHeight + blendLength)) 
		# Bottom fill

	for y in range(imageHeight - 1):
		pixel = image.getpixel((0, y))
		borderedImage.paste(Image.new('RGB', (blendLength, 1), pixel), (0, blendLength + y)) 
		# Left fill

		pixel = image.getpixel((imageWidth - 1, y))	
		borderedImage.paste(Image.new('RGB', (blendLength, 1), pixel), (imageWidth + blendLength, blendLength + y)) 
		# Right fill

	cornerFillSize = (blendLength, blendLength)

	pixel = borderedImage.getpixel((blendLength, blendLength))
	borderedImage.paste(Image.new('RGB', cornerFillSize, pixel), (0, 0))
	# Top left corner fill

	pixel = borderedImage.getpixel((blendLength, blendLength + imageHeight))
	borderedImage.paste(Image.new('RGB', cornerFillSize, pixel), (0, blendLength + imageHeight - 1))
	# Bottom left corner fill

	pixel = borderedImage.getpixel((blendLength + imageWidth, blendLength))
	borderedImage.paste(Image.new('RGB', cornerFillSize, pixel), (blendLength + imageWidth, 0))
	# Top right corner fill

	pixel = borderedImage.getpixel((blendLength + imageWidth - 1, blendLength + imageHeight - 1))
	borderedImage.paste(Image.new('RGB', cornerFillSize, pixel), (blendLength + imageWidth, blendLength + imageHeight - 1))
	# Bottom right corner fill
	
	return borderedImage




