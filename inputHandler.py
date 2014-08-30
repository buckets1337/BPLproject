#inputHandler.py
#handles user input events

import pygame
import sys
from pygame.locals import *


class InputHandler():
	def __init__(self):
		pass

	def handleEvents(self, gameState, gameEngine, screen):
		'''
		handles input events
		'''
		if gameState == 'normal':
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit()
					if event.key == K_SPACE:
						gameState = gameEngine.turn(gameState)
					if event.key == K_F12:
						screen = self.toggle_fullscreen()
		return screen, gameState

	def toggle_fullscreen(self):
		screen = pygame.display.get_surface()
		tmp = screen.convert()

		cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
		
		w,h = screen.get_width(),screen.get_height()
		flags = screen.get_flags()
		bits = screen.get_bitsize()
		
		pygame.display.quit()
		pygame.display.init()
		
		screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
		screen.blit(tmp,(0,0))
	 
		pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
	 
		pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
		
		return screen
