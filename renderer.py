#renderer.py
#refreshes the screen

# import the needed modules and libraries.
import pygame
import os, random
import CONFIG


# A Renderer is an 'invisible' object that draws things to the screen.  Without this, our screen will always be black and empty
class Renderer():
    '''
    A renderer is responsible for drawing all objects to the screen, except the message console in the middle
    '''

    # set the rnderer up, telling what the screen is, what needs to be drawn, and setting a background image.
    def __init__(self, screen, renderList):
        self.screen = screen
        self.renderList = renderList
        self.loadImages()
        self.backgroundSelected = False
        self.background = None
        self.redSurf = None
        self.blueSurf = None
        self.defaultFont = pygame.font.SysFont('monospace', 16)


    # loads in a default image for mechs that do not have images specified.
    def loadImages(self):
        self.mechImage = pygame.image.load(CONFIG.IMAGE_PATH + 'mech.png')
        self.mechImage.convert()
        self.mechImage = pygame.transform.scale(self.mechImage, (64,64))
        self.tinyMechImage = pygame.transform.scale(self.mechImage, (32,32))


    # This code is called each time through the main loop.  It merely instructs the renderer to draw other things to the screen.
    def render(self, gameState, screen, imageList, redList, blueList, console, initiativeOrder):
        '''
        called when the screen refreshes each frame.  Clears the screen and then redraws it
        '''

        # fill the screen with black, to 'erase' information from the last time through the main loop
        screen.fill(CONFIG.BLACK)

        # this is a list of all the things the renderer redraws each time through the main loop.  Thus, all of this is drawn to the screen,
        # 20 times each second by default.
        self.renderField(screen)
        self.renderSides(screen)
        self.renderConsole(screen, console)
        self.renderMechs(screen, redList, 50)
        self.renderMechs(screen, blueList, 900)
        self.renderInitiativeOrder(screen, initiativeOrder)

        # now that everything is drawn to the screen, tell it to go ahead and update so that we see the results of drawing to the screen.
        pygame.display.flip()


    # draw the mechs to the screen
    def renderMechs(self, screen, mechList, startingX):

        # sets the coordinates on screen for the first mech
        xpos = startingX
        ypos = 10

        # for each mech in the game, draw it to the screen
        for item in mechList:
            if item.image != None:
                screen.blit(item.image, (xpos,ypos))
            else:
                screen.blit(self.mechImage, (xpos, ypos))

            # draw the mech's health bar, heat bar, and name.
            self.renderHealthBar(screen, item, xpos - 10, ypos)
            self.renderHeatBar(screen, item, xpos + 64 + 5, ypos)
            self.renderName(screen, item, xpos, ypos + 70)

            # move down far enough to make room for drawing the next mech
            ypos += 128


    # draws a mech's health bar to the screen
    def renderHealthBar(self, screen, mech, xpos, ypos):

        # the health bar consists of two rectangles.  The rectangle drawn first (on the bottom), represents the maximum health a mech can have.
        # the rectangle drawn second (on the top) represents what fraction of the max health the mech still has remaining.
        startingHealth = (mech.armor * 2.0) + 2
        healthPercent = int((mech.health / startingHealth)*64)
        lostHealthPercent = 64-healthPercent
        background = pygame.Rect(xpos, ypos, 5, 64)
        healthBar = pygame.Rect(xpos, ypos + lostHealthPercent, 5, healthPercent)

        backSurf = pygame.Surface((background.w, background.h))
        backSurf.fill(CONFIG.WHITE)

        healthSurf = pygame.Surface((healthBar.w, healthBar.h))
        healthSurf.fill(CONFIG.DARK_GREEN)

        # now that the sizes of the rectangles have been determined, draw them to the screen
        screen.blit(backSurf, background)
        screen.blit(healthSurf, healthBar)


    # draws a mech's heat bar to the screen.  The heat bar works the same as the health bar, except that it shows the heat stat instead of the health stat.
    def renderHeatBar(self, screen, mech, xpos, ypos):
        heatPercent = int((mech.heat/CONFIG.HEAT_LIMIT)*64)
        if heatPercent < 1:
            heatPercent = 1
        if heatPercent > 64:
            heatPercent = 64
        lostHeatPercent = 64-heatPercent

        background = pygame.Rect(xpos, ypos, 5, 64)
        heatBar = pygame.Rect(xpos, ypos + lostHeatPercent, 5, heatPercent)

        backSurf = pygame.Surface((background.w, background.h))
        backSurf.fill(CONFIG.WHITE)

        heatSurf = pygame.Surface((heatBar.w, heatBar.h))
        heatSurf.fill(CONFIG.ORANGE)

        screen.blit(backSurf, background)
        screen.blit(heatSurf, heatBar)


    # draw the message console to the center of the screen
    def renderConsole(self, screen, console):

        # set the size and location of the console
        ypos = console.ypos + console.height
        w = CONFIG.SCREEN_SIZE[0] - 330
        h = CONFIG.SCREEN_SIZE[1]
        background = pygame.Surface((w, h))

        # clear the console by filling it with black
        background.fill(CONFIG.BLACK)

        # make the console slightly transparent, showing the background below it
        background.set_alpha(180)
        screen.blit(background, (console.xpos-15, 0))

        # for each message the console has received, draw it to the screen, then move down.  The newest message will be at the bottom of the console, and
        # the oldest message will be at the top.
        for message in console.messageList:
            messageSurf = self.defaultFont.render(message, True, CONFIG.WHITE)
            screen.blit(messageSurf, (console.xpos, ypos))
            ypos -= 16


    # draw each teams' side, giving it a colored tint to represent the side
    def renderSides(self, screen):

        # if the side isn't already present, determine the size of the side
        if self.redSurf == None or self.blueSurf == None:
            totalSides = 330
            sideLength = int(totalSides / 2)
            self.sideLength = sideLength

            # if the red side isn't present, draw it
            if self.redSurf == None:
                redSurf = pygame.Surface((sideLength, CONFIG.SCREEN_SIZE[1]))
                redSurf.fill(CONFIG.DARK_RED)
                redSurf.set_alpha(100)
                self.redSurf = redSurf

            # if the blue side isn't present, draw it
            if self.blueSurf == None:
                blueSurf = pygame.Surface((sideLength, CONFIG.SCREEN_SIZE[1]))
                blueSurf.fill(CONFIG.DARK_BLUE)
                blueSurf.set_alpha(100)
                self.blueSurf = blueSurf

        # go ahead and draw both sides to the main sreen
        screen.blit(self.redSurf,(0,0))
        screen.blit(self.blueSurf,(CONFIG.SCREEN_SIZE[0]-self.blueSurf.get_width(), 0))


    # pick a background image randomly from those present in the 'battlefields' directory, and then render it to the screen
    def renderField(self, screen):
        if not self.backgroundSelected:
            backgroundList = os.listdir(CONFIG.IMAGE_PATH + "battlefields/")
            numBackgrounds = len(backgroundList)
            choice = random.randint(0,numBackgrounds-1)
            imageName = backgroundList[choice]
            background = pygame.image.load(CONFIG.IMAGE_PATH+"battlefields/" +imageName)
            background.convert()
            background = pygame.transform.scale(background, CONFIG.SCREEN_SIZE)
            self.background = background
            self.backgroundSelected = True
        screen.blit(self.background, (0,0))


    # draw the name of a mech to the screen
    def renderName(self, screen, mech, xpos, ypos):
        nameSurf = self.defaultFont.render(mech.name, True, CONFIG.WHITE)
        screen.blit(nameSurf, (xpos, ypos))


    # draws the initiative queue at the top of the screen
    def renderInitiativeOrder(self, screen, initiativeOrder):
        # set size and location for the queue
        initSurf = pygame.Surface((675, 48))
        initSurf.fill(CONFIG.BLACK)
        xloc = 32
        # for each mech, determine which team it is on and give it a colored background.  Then, on top of that
        # colored background, draw a tiny verson of the mech's picture
        for mech in initiativeOrder:
            if mech.team == "Red":
                imgBack = pygame.Surface((36,36))
                imgBack.fill(CONFIG.RED)

            elif mech.team == "Blue":
                imgBack = pygame.Surface((36,36))
                imgBack.fill(CONFIG.BLUE)

            initSurf.blit(imgBack, (xloc-2, 6))

            # if the mech doesn't have a tiny image, give it the default
            if mech.tinyImage != None:
                initSurf.blit(mech.tinyImage, (xloc, 8))
            else:
                initSurf.blit(self.tinyMechImage, (xloc, 8))
            xloc += 48

        # draw the initiative queue to the main screen
        screen.blit(initSurf, (175, 0))


    # This can be ignored, as animation is not yet in the game
    def renderAnimation(self):
        '''
        draws an animation to the screen
        '''
        pass


# the Console object is the message console displayed in the center of the screen
class Console():
    # set up the console, letting it know what dimensions to use, and giving it a list to store the messages in
    def __init__(self, xpos, ypos, width, height):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

        self.messageList = []
