# demoPixelArray.py
# and example of a PixelArray definition

## This first section is boilerplate.  This code should be in your script, unchanged.

# make sure pygame is loaded, even though it likely is from whatever is calling this array
import pygame
# call in CONFIG.py for the color definitions
import CONFIG

# make sure pygame is initialized
pygame.init()

## END BOILERPLATE



class exampleArray():
	'''
	This is an example of a pixelArray object.  This would be used in the game as your player portrait
	'''

	def __init__(self):

		# First, define any colors we may need, if they are not already in CONFIG.py
		self.GREY = (84,84,84)
		self.LIGHT_GREY = (150,150,150)

		# ake a surface that we will draw pixels on.  It can be any size, but it will be re-formed to be 64x64 in the game.
		# Here, I used 19x23 as my size, because that is the size of the pixel art I am using for my picture
		self.surf = pygame.Surface((19,23))

		# fill the surface with a light grey background.  We could do any color here really, I just chose light grey
		self.surf.fill(self.LIGHT_GREY)

		# next, wrap the surface in a pixelArray, so that we can directly access the pixels of the surface
		self.pixelArray = pygame.PixelArray(self.surf)

		# let the pixelArray know what pixels should be what color
		self.defineColors()

		# color in the pixels in the pixelArray, using the lists created by defineColors()
		self.colorArray(self.BLACK_PIXELS, CONFIG.BLACK)
		self.colorArray(self.WHITE_PIXELS, CONFIG.WHITE)
		self.colorArray(self.GREY_PIXELS, self.GREY)
		self.colorArray(self.BLUE_PIXELS, CONFIG.BLUE)
		self.colorArray(self.RED_PIXELS, CONFIG.RED)


	def defineColors(self):
		# now, we can assign colors to the pixels in our surface to create the image. We will do this by creating lists, with each
		# list containing the coordinates of pixels of one color. 

		self.BLACK_PIXELS = [(8,0), (9,0), (10,0), (6,1), (7,1), (11,1), (12,1), (5,2), (13,2), (4,3), (4,4), (14,3), (14,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (3,13), (3,14), (3,15), (3,16),
			(15,5), (15,6), (15,7), (15,8), (15,9), (15,10), (15,11), (15,12), (15,13), (15,14), (15,15), (15,16), (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8), (14,8),
			(15,8), (16,8), (17,8), (0,9), (0,10), (0,11), (1,10), (18,9), (18,10), (18,11), (17,10), (1,12), (1,13), (1,14), (1,15), (1,16), (1,17), (1,18), (1,19), (17,12), (17,13), (17,14), (17,15), (17,16),
			(17,17), (17,18), (17,19), (2,16), (16,16), (4,16), (5,16), (7,16), (8,16), (9,16), (10,16), (11,16), (13,16), (14,16), (4,17), (14,17), (4,18), (5,18), (6,18), (7,18), (8,18), (9,18), (10,18), (11,18),
			(12,18), (13,18), (14,18), (7,5), (6,6), (7,6), (9,1), (8,2), (9,2), (10,2), (9,3), (0,19), (1,19), (2,19), (3,19), (4,19), (7,19), (11,19), (14,19), (15,19), (16,19), (17,19), (18,19), (0,20), (3,20), 
			(6,20), (7,20), (8,20), (9,20), (10,20), (11,20), (12,20), (15,20), (18,20), (0,21), (4,21), (6,21), (9,21), (12,21), (14,21), (18,21), (0,22), (1,22), (2,22), (3,22), (4,22), (6,22), (7,22), (8,22),
			(9,22), (10,22), (11,22), (12,22), (14,22), (15,22), (16,22), (17,22), (18,22), (8,12), (9,12), (10,12), (8,14), (9,14), (10,14)]

		self.WHITE_PIXELS = [(6,2), (12,2), (5,3), (6,3), (7,3), (11,3), (12,3), (13,3), (5,4), (8,4), (9,4), (10,4), (11,4), (12,4), (13,4), (4,5), (6,5), (11,5), (14,5), (4,6), (11,6), (14,6), (4,7), (5,7),
			(6,7), (7,7), (8,7), (9,7), (10,7), (11,7), (12,7), (13,7), (14,7), (1,9), (2,9), (4,9), (5,9), (6,9), (8,9), (9,9), (10,9), (12,9), (13,9), (14,9), (16,9), (17,9), (2,10), (6,10), (12,10), (16,10),
			(1,11), (2,11), (4,11), (6,11), (7,11), (8,11), (9,11), (10,11), (11,11), (12,11), (14,11), (16,11), (17,11), (4,12), (6,12), (7,12), (11,12), (12,12), (14,12), (6,13), (7,13), (8,13), (9,13), (10,13),
			(11,13), (12,13), (4,14), (6,14), (7,14), (11,14), (12,14), (14,14), (6,15), (7,15), (8,15), (9,15), (10,15), (11,15), (12,15), (6,16), (12,16), (3,17), (5,17), (6,17), (7,17), (9,17), (11,17), (12,17),
			(13,17), (15,17), (2,18), (3,18), (15,18), (16,18), (8,19), (9,19), (10,19), (1,20), (17,20), (1,21), (2,21), (3,21), (7,21), (8,21), (10,21), (11,21), (15,21), (16,21), (17,21)]

		self.GREY_PIXELS = [(7,9), (11,9), (4,10), (5,10), (7,10), (8,10), (9,10), (10,10), (11,10), (13,10), (14,10), (5,11), (13,11), (5,12), (13,12), (4,13), (5,13), (13,13), (14,13), (5,14), (13,14), (4,15), (5,15), 
			(13,15), (14,15), (2,20), (16,20)]

		self.BLUE_PIXELS = [(8,1), (10,1), (7,2), (11,2), (8,3), (10,3), (6,4), (7,4), (5,5), (8,5), (9,5), (10,5), (12,5), (13,5), (5,6), (8,6), (10,6), (12,6), (13,6), (2,12), (2,13), (2,14), (2,15), (2,17), (16,12), (16,13),
			(16,14), (16,15), (16,17)]

		self.RED_PIXELS = [(9,6), (8,17), (10,17)]


	def colorArray(self, pixelList, color):
		# using the list of coordinates, we now go through and apply the color to each pixel in self.pixelArray
		for pixel in pixelList:
			self.pixelArray[pixel[0], pixel[1]] = color
		