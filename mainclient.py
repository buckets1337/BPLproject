#mainclient.py
#handles the display and user input

import pygame
from pygame.locals import *
import inputHandler, renderer, fileLoader, gameEngine
import CONFIG



pygame.init()

screen = pygame.display.set_mode(CONFIG.SCREEN_SIZE)
renderList = []

RenderEngine = renderer.Renderer(screen, renderList)
InputHandler = inputHandler.InputHandler()
FileLoader = fileLoader.FileLoader()
Console = renderer.Console(180,10,80,700)

avatarListRed = FileLoader.loadFromFile(CONFIG.RED_TEAM_PATH, 'Red', Console)
avatarListBlue = FileLoader.loadFromFile(CONFIG.BLUE_TEAM_PATH, 'Blue', Console)

GameEngine = gameEngine.GameEngine(avatarListRed, avatarListBlue, Console)

Clock = pygame.time.Clock()




while True:

    Clock.tick(20)

    screen = InputHandler.handleEvents(GameEngine, screen)

    RenderEngine.render(screen, renderList, avatarListRed, avatarListBlue, Console, GameEngine.initiativeOrder)








