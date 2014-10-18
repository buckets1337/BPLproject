#mainclient.py
#handles the display and user input


# this section imports modules and libraries needed to make the game work, including pygame.  Pygame gives
# us the ability to check for keyboard presses, as well as draw whatever we want in a window.  Basically, 
# pygame is a toolbox for creating computer games.  Without pygame, we would not have a way to check if
# a key on the keyboard has been pressed, or to draw anything on the screen.  Thus, pygame gives us the
# ability to allow someone to actually play the game!  We also import the other game files, and the CONFIG
# file.
import pygame
from pygame.locals import *
import inputHandler, renderer, fileLoader, gameEngine
import CONFIG



# start pygame.  This has to be done before the parts of pygame we use will work.  This runs before ANY other code
# in the game is able to run.
pygame.init()

# here we define the 'screen', which is the window the game is drawn in, and provide it a size from CONFIG.py
screen = pygame.display.set_mode(CONFIG.SCREEN_SIZE)

# here we create a 'renderList', in order to keep track of everything that we want to draw in our game window as the game runs.
renderList = []

# this tells the computer that the game has not yet ended.  If gameState is not 'normal', the game will stop running.
gameState = 'normal'


# Here we create a Renderer object, as described by renderer.py.  The Renderer object is 'invisible', and will never show up
# to our players.  However, it does handle drawing everything we *do* see on the screen, so we create it before the main loop
# starts, giving our game some way to draw everything.
RenderEngine = renderer.Renderer(screen, renderList)

# Here we create another 'invisible' object, the InputHandler object, as described in inputHandler.py.  The input handler simply checks if a key has been pressed,
# and then directs the computer to the correct code to run if a key has been pressed.  Without an 'InputHandler', the keyboard would not work.
InputHandler = inputHandler.InputHandler()

# This creates yet another 'invisible' object, the FileLoader, as described by fileLoader.py.  The fileLoader object will load information
# from files into the game, setting the stats of the mechs and giving them names and pictures.
FileLoader = fileLoader.FileLoader()

# This creates a Console object.  The Console object displays the text about what is happening in the game that you see in the middle of the window.  Without this 
# console, it is difficult to tell what is happening in the game.
Console = renderer.Console(180,10,80,700)

# These two lists represent the mechs on each team.  The FileLoader object that we created earlier is used to pull the stats in, but we actually keep track of the
# teams using these two lists.  Once all mechs have been killed and removed from a list, the game ends, and the team with mechs still on their list is the winner.
avatarListRed = FileLoader.loadFromFile(CONFIG.RED_TEAM_PATH, 'Red', Console)
avatarListBlue = FileLoader.loadFromFile(CONFIG.BLUE_TEAM_PATH, 'Blue', Console)

# This creates another 'invisible' object, the GameEngine.  The GameEngine object tells the computer what to do when the InputHandler object has detected that a key
# was pressed on the keyboard.
GameEngine = gameEngine.GameEngine(avatarListRed, avatarListBlue, Console)

# Here we create the game clock, which is mostly responsible for telling the computer how many times the main loop should be run each second.
Clock = pygame.time.Clock()




### MAIN GAME LOOP ###

# this code will repeat over and over, until our game has ended.  This is the section that actually makes the game 'go'.  Nearly every game has a main game loop, so
# learning how this works will help you in understanding how other types of games are made.
while True:			# This will always happen, so the loop runs forever, until we quit the game or close the game window.

	# This line tells the computer how many times the main loop should run in each second.  If you change this line by switching out the '20' for another number, you can
	# change how fast the loop runs.  For example, if you change the line to read 'Clock.tick(60)', the game will run through the main loop 60 times each second instead.
    Clock.tick(20)

    # Once per main loop, we check to see if a key on the keyboard has been pressed.  If it has, the InputHandler object will tell the GameEngine object which key was pressed,
    # and the GameEngine object will then run some code that causes things to happen (deal damage, reload, die, etc).  The InputHandler returns information to us about how large
    # the game window should be, and whether the game should still be running.
    screen, gameState = InputHandler.handleEvents(gameState, GameEngine, screen)

    # Once any key presses have been resolved by InputHandler and GameEngine, the RenderEngine we set up earlier will redraw the screen, illustrating any changes made due to 
    # key presses.  This runs once per main loop, therefore, we get 20 'frames' per second by default.
    RenderEngine.render(gameState, screen, renderList, avatarListRed, avatarListBlue, Console, GameEngine.initiativeOrder)


### END MAIN GAME LOOP ###
