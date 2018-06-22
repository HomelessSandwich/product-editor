from PIL import Image, ImageOps
from operator import itemgetter

def GetTopPixel(threshold, image, rgbImgWidth, rgbImgHeight):
	topPixel = (0, 0)
	for i in range(rgbImgHeight):
		for j in range(rgbImgWidth):
			r, g, b = image.getpixel((j, i))		
			if not r or not b or not g > threshold * 255:
				topPixel = (j , i)
				return topPixel

def GetBottomPixel(threshold, image, rgbImgWidth, rgbImgHeight):
	bottomPixel = (0, 0)
	for i in reversed(range(rgbImgHeight)):
		for j in reversed(range(rgbImgWidth)):
			r, g, b = image.getpixel((j, i))		
			if not r or not b or not g > threshold * 255:
				bottomPixel = (j , i)
				return bottomPixel

def GetLeftPixel(threshold, image, rgbImgWidth, rgbImgHeight):
	leftPixel = (0, 0)
	for i in range(rgbImgWidth):
		for j in range(rgbImgHeight):
			r, g, b = image.getpixel((i, j))		
			if not r or not b or not g > threshold * 255:
				leftPixel = (i , j)
				return leftPixel
				
def GetRightPixel(threshold, image, rgbImgWidth, rgbImgHeight):
	rightPixel = (0, 0)
	for i in reversed(range(rgbImgWidth)):
		for j in reversed(range(rgbImgHeight)):
			r, g, b = image.getpixel((i, j))		
			if not r or not b or not g > threshold * 255:
				rightPixel = (i , j)
				return rightPixel

def FindEdges(threshold, image):
	rgbImg = image.convert('RGB')
	rgbImgWidth, rgbImgHeight = rgbImg.size

	topPixel = GetTopPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight)
	bottomPixel = GetBottomPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight)
	leftPixel = GetLeftPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight)
	rightPixel = GetRightPixel(threshold, rgbImg, rgbImgWidth, rgbImgHeight)

	return topPixel, bottomPixel, leftPixel, rightPixel

def CropImage(topPixel, bottomPixel, leftPixel, rightPixel, image):
	image = image.crop((leftPixel[0], topPixel[1], rightPixel[0], bottomPixel[1]))
	return image
