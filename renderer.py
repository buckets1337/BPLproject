#renderer.py
#refreshes the screen

import pygame
import os, random
import CONFIG


class Renderer():
    def __init__(self, screen, renderList):
        self.screen = screen
        self.renderList = renderList
        self.loadImages()
        self.backgroundSelected = False
        self.background = None
        self.redSurf = None
        self.blueSurf = None

        self.defaultFont = pygame.font.SysFont('monospace', 16)


    def loadImages(self):
        self.mechImage = pygame.image.load(CONFIG.IMAGE_PATH + 'mech.png')
        self.mechImage.convert()
        self.mechImage = pygame.transform.scale(self.mechImage, (64,64))
        self.tinyMechImage = pygame.transform.scale(self.mechImage, (32,32))


    def render(self, gameState, screen, imageList, redList, blueList, console, initiativeOrder):
        '''
        called when the screen refreshes each frame.  Clears the screen and then redraws it
        '''

        screen.fill(CONFIG.BLACK)

        self.renderField(screen)
        self.renderSides(screen)
        self.renderConsole(screen, console)
        self.renderMechs(screen, redList, 50)
        self.renderMechs(screen, blueList, 900)
        self.renderInitiativeOrder(screen, initiativeOrder)

        pygame.display.flip()


    def renderMechs(self, screen, mechList, startingX):
        xpos = startingX
        ypos = 10
        for item in mechList:
            if item.image != None:
                screen.blit(item.image, (xpos,ypos))
            else:
                screen.blit(self.mechImage, (xpos, ypos))

            self.renderHealthBar(screen, item, xpos - 10, ypos)
            self.renderHeatBar(screen, item, xpos + 64 + 5, ypos)
            self.renderName(screen, item, xpos, ypos + 70)
            ypos += 128


    def renderHealthBar(self, screen, mech, xpos, ypos):
        startingHealth = (mech.armor * 2.0) + 2
        healthPercent = int((mech.health / startingHealth)*64)
        #print mech.ID, mech.health, healthPercent
        lostHealthPercent = 64-healthPercent
        background = pygame.Rect(xpos, ypos, 5, 64)
        healthBar = pygame.Rect(xpos, ypos + lostHealthPercent, 5, healthPercent)

        backSurf = pygame.Surface((background.w, background.h))
        backSurf.fill(CONFIG.WHITE)

        healthSurf = pygame.Surface((healthBar.w, healthBar.h))
        healthSurf.fill(CONFIG.DARK_GREEN)

        screen.blit(backSurf, background)
        screen.blit(healthSurf, healthBar)


    def renderHeatBar(self, screen, mech, xpos, ypos):
        heatPercent = int((mech.heat/CONFIG.HEAT_LIMIT)*64)
        if heatPercent < 1:
            heatPercent = 1
        if heatPercent > 64:
            heatPercent = 64
        lostHeatPercent = 64-heatPercent
        #print mech.ID, (mech.heat/CONFIG.HEAT_LIMIT), heatPercent

        background = pygame.Rect(xpos, ypos, 5, 64)
        heatBar = pygame.Rect(xpos, ypos + lostHeatPercent, 5, heatPercent)

        backSurf = pygame.Surface((background.w, background.h))
        backSurf.fill(CONFIG.WHITE)

        heatSurf = pygame.Surface((heatBar.w, heatBar.h))
        heatSurf.fill(CONFIG.ORANGE)

        screen.blit(backSurf, background)
        screen.blit(heatSurf, heatBar)


    def renderConsole(self, screen, console):
        ypos = console.ypos + console.height
        w = CONFIG.SCREEN_SIZE[0] - 330
        h = CONFIG.SCREEN_SIZE[1]
        background = pygame.Surface((w, h))
        background.fill(CONFIG.BLACK)
        background.set_alpha(180)
        screen.blit(background, (console.xpos-15, 0))
        for message in console.messageList:
            messageSurf = self.defaultFont.render(message, True, CONFIG.WHITE)
            screen.blit(messageSurf, (console.xpos, ypos))
            ypos -= 16


    def renderSides(self, screen):
        if self.redSurf == None or self.blueSurf == None:
            totalSides = 330
            sideLength = int(totalSides / 2)
            self.sideLength = sideLength
            if self.redSurf == None:
                redSurf = pygame.Surface((sideLength, CONFIG.SCREEN_SIZE[1]))
                redSurf.fill(CONFIG.DARK_RED)
                redSurf.set_alpha(100)
                self.redSurf = redSurf
            if self.blueSurf == None:
                blueSurf = pygame.Surface((sideLength, CONFIG.SCREEN_SIZE[1]))
                blueSurf.fill(CONFIG.DARK_BLUE)
                blueSurf.set_alpha(100)
                self.blueSurf = blueSurf
        screen.blit(self.redSurf,(0,0))
        screen.blit(self.blueSurf,(CONFIG.SCREEN_SIZE[0]-self.blueSurf.get_width(), 0))


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


    def renderName(self, screen, mech, xpos, ypos):
        nameSurf = self.defaultFont.render(mech.name, True, CONFIG.WHITE)
        screen.blit(nameSurf, (xpos, ypos))


    def renderInitiativeOrder(self, screen, initiativeOrder):
        initSurf = pygame.Surface((675, 48))
        initSurf.fill(CONFIG.BLACK)
        xloc = 32
        for mech in initiativeOrder:
            if mech.team == "Red":
                imgBack = pygame.Surface((36,36))
                imgBack.fill(CONFIG.RED)

            elif mech.team == "Blue":
                imgBack = pygame.Surface((36,36))
                imgBack.fill(CONFIG.BLUE)

            initSurf.blit(imgBack, (xloc-2, 6))

            if mech.tinyImage != None:
                initSurf.blit(mech.tinyImage, (xloc, 8))
            else:
                initSurf.blit(self.tinyMechImage, (xloc, 8))
            xloc += 48


        screen.blit(initSurf, (175, 0))


    def renderAnimation(self):
        '''
        draws an animation to the screen
        '''
        pass


class Console():
    def __init__(self, xpos, ypos, width, height):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

        self.messageList = []
