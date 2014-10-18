#inputHandler.py
#handles user input events

# import the libraries and modules required for this script
import pygame
import sys
from pygame.locals import *


# An InputHandler object is an 'inivisble' object that checks to see if a key has been pressed
# on the keyboard.  If a key has been pressed, InputHandler will tell the computer what code to 
# run in order to make things happen
class InputHandler():

	# an InputHandler doesn't have any stats to set up when it is first made
	def __init__(self):
		pass


	# Look for any keys pressed on the keyboard.  If a key has been pressed, make something happen.
	def handleEvents(self, gameState, gameEngine, screen):
		'''
		handles input events
		'''

		# if the game has not ended, look for a key press.
		if gameState == 'normal':
			for event in pygame.event.get():

				# if the window is closed, end the program
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == KEYDOWN:
					# if the 'esc' key is pressed, end the program
					if event.key == K_ESCAPE:
						sys.exit()
					# if the spacebar is pressed, tell the GameEngine object to process the next round
					if event.key == K_SPACE:
						gameState = gameEngine.turn(gameState)
					# if the 'F12' key is pressed, toggle fullscreen (ie, if the game is in a window, go to fullscreen, and vice-versa).
					if event.key == K_F12:
						screen = self.toggle_fullscreen()
		# return some info about the screen and whether tha game has ended
		return screen, gameState


	# This describes a method to go from fullscreen to a window, and from a window to fullscreen.  The details are unimportant, just know
	# that if this code is called, fullscreen is toggled from the state it is in to the other state.
	def toggle_fullscreen(self):
		screen = pygame.display.get_surface()
		tmp = screen.convert()

		cursor = pygame.mouse.get_cursor()  
		
		w,h = screen.get_width(),screen.get_height()
		flags = screen.get_flags()
		bits = screen.get_bitsize()
		
		pygame.display.quit()
		pygame.display.init()
		
		screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
		screen.blit(tmp,(0,0))
	 
		pygame.key.set_mods(0) 
	 
		pygame.mouse.set_cursor( *cursor )  
		
		return screen
