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

def GetBufferPixels(topPixel, bottomPixel, leftPixel, rightPixel, image):
	imageWidth, imageHeight = image.size

	if leftPixel[0] - round(0.01 * imageWidth) >= 0:
		leftPixel = (leftPixel[0] - round(0.01 * imageWidth), leftPixel[1])
	else:
		leftPixel = (0, leftPixel[1])
	if topPixel[1] - round(0.01 * imageHeight) >= 0:
		topPixel = (topPixel[0], topPixel[1] - round(0.01 * imageHeight))
	else:
		topPixel = (topPixel[0], 0)
	if rightPixel[0] + round(0.01 * imageWidth) <= imageWidth:
		rightPixel = (rightPixel[0] + round(0.01 * imageWidth), rightPixel[1])
	else:
		rightPixel = (imageWidth, rightPixel[1])
	if bottomPixel[1] + round(0.01 * imageWidth) <= imageHeight:
		bottomPixel = (bottomPixel[0], bottomPixel[1] + round(0.01 * imageHeight))
	else:
		bottomPixel = (bottomPixel[0], imageHeight)
	# Buffers away from the detected edges to avoid small clipping
	return leftPixel, topPixel, rightPixel, bottomPixel

def BlendBackgrounds(image, backgroundColour):
	image = image.convert('RGB')
	imageWidth, imageHeight = image.size
	buffLeftPixel, buffTopPixel, buffRightPixel, buffBottomPixel = GetBufferPixels(topPixel, bottomPixel, leftPixel, rightPixel, image)
	backgroundSnippet = Image.new('RGB', (10, topPixel[1] - buffTopPixel[1]), backgroundColour)

	test = Image.new('RGB', (10, topPixel[1] - buffTopPixel[1]), (255, 0, 0))

	for x in range(0, buffRightPixel[0] - buffLeftPixel[0] + 10, 10):
		snippet = image.crop((buffLeftPixel[0] + x, buffTopPixel[1], buffLeftPixel[0] + x + 10, buffTopPixel[1] + (topPixel[1] - buffTopPixel[1])))
		blendedSnippet = Image.blend(snippet, backgroundSnippet, 0.5)
		image.paste(test, (buffLeftPixel[0] + x, buffTopPixel[1]))

	return image

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
	# Finds the location on the image for image2 to be centred
	image.paste(image2, (locationX, locationY))
	return image