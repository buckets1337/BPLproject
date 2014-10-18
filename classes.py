#classes
#class definitions

# import modules and libraries needed by this file.
import random, time
import pygame
import fileLoader, IDs, CONFIG


# start pygame, just in case it wasn't yet started by 'mainclient.py'
pygame.init()


# This defines an 'Avatar', which is a representation of a single player and his/her mech.  Think of 'Avatars' as game pieces.  They deal and take the damage,
# and once all the 'Avatars' on one team have died, the game ends.
class Avatar():
    '''
    an avatar is a representation of a player.  It is constructed from data obtained from the RFID readers, and does the battling.
    '''

    # Here we describe the initial settings of a mech when it is created.  This is a good place to look if you wnat to see what stats each mech actually has
    def __init__(self, rfidString, team, console):
        # creates a fileLoader for the mech, so that it can load in the mech's stats
        self.FileLoader = fileLoader.FileLoader()

        # let the mech know it's team
        self.team = team
        # tell the mech where the console is
        self.console = console
        # give the mech it's stats
        self.definition = rfidString
        # set a unique ID for the mech, so we can tell which one it is in a list of the other mechs
        self.ID = self.definition[0] + self.definition[1]
        # tell the mech which player's name it has
        self.name = IDs.playerList[int(self.ID)-1][0]

        # set up a small version of the player's picture
        self.tinyImage = None
        if IDs.playerList[int(self.ID)-1][1] != None:
            self.image = IDs.playerList[int(self.ID)-1][1]
        else:
            self.image = None

        if IDs.playerList[int(self.ID)-1][2] != None:
            self.pixelArray = IDs.playerList[int(self.ID)-1][2]
        else:
            self.pixelArray = None

        # set the picture for the mech
        if self.image != None:
            self.loadImage()
        if self.pixelArray != None:
            self.loadImage(pixelArray=self.pixelArray, pixelArrayLocation=CONFIG.PIXEL_ARRAY_PATH)

        # in this section, we assign the stats to the mech.  These stats are all derived from the file created by RFIDreader.py and loaded in by the mech's FileLoader object
        self.heatSinks = int(self.definition[2])
        self.armor = int(self.definition[3])
        self.weapon1ID = self.definition[4:6]
        self.weapon2ID = self.definition[6:8]
        self.weapon3ID = self.definition[8:10]
        self.weapon4ID = self.definition[10:12]
        self.health = (self.armor*2) + 2
        self.target = None
        self.damageTaken = 0
        self.heat = 0
        self.weapons = []
        self.setupWeapons()
        self.coolOff = False
        initMod = random.randrange(75,125)
        self.initiative = int((self.evasion * initMod) / 100)


    # here we tell the mech how to figure out what value it has for the 'cooling' stat, even though that stat isn't in the file that the FileLoader loaded for it
    @property
    def cooling(self):
        # the cooling stat is determined entirely by how many heat sinks it has.
        cooling = self.heatSinks + 1
        return cooling


    # and here we tell the mech how to figure out what value it has for the 'evasion' stat.
    @property
    def evasion(self):
        # initially, the mech's evasion is equal to the value set in CONFIG.py
        evasion = CONFIG.BASE_EVASION
        # if the mech has armor, make it less evasive
        if self.armor != 0:
            evasion -= (2*self.armor)
        # if the mech has heat sinks (for cooling), make it less evasive
        if self.heatSinks != 0:
            evasion -= self.heatSinks
        # if the mech has weapons, make the mech less evasive for each weapon it has equipped
        for weapon in self.weapons:
            if weapon != None:
                evasion -= weapon.speedPenalty

        return evasion



    # This handles loading in the player image to the mech.  It will redirect the computer to the instructions you wrote to draw your picture.
    def loadImage(self, pixelArray = None, pixelArrayLocation = None):
        '''
        loads a custom image as defined in IDs.py
        '''
        if pixelArray == None:
            imagePath = self.image
            self.image = pygame.image.load(CONFIG.IMAGE_PATH + imagePath)
            self.image.convert()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.tinyImage = pygame.transform.scale(self.image, (32, 32))
        else:
            pixelArrayList = self.FileLoader.loadPixelArrays(pixelArrayLocation)
            self.imageObj = pixelArrayList[pixelArray].exampleArray()
            self.image = self.imageObj.surf
            self.image.convert()
            self.image = pygame.transform.scale(self.image, (64,64))
            self.tinyImage = pygame.transform.scale(self.image, (32,32))



    # This section sets up the weapons that a mech has equipped.  Each possible weapon must be defined here, or else it won't work.
    def setupWeapons(self):
        '''
        configures the mech's weapons when the mech is created
        '''
        
        weaponDefList = self.FileLoader.loadWeaponModules('Weapons')
        newWeapon1ID = CONFIG.WEAPON_REGISTER[int(self.weapon1ID)]
        newWeapon2ID = CONFIG.WEAPON_REGISTER[int(self.weapon2ID)]
        newWeapon3ID = CONFIG.WEAPON_REGISTER[int(self.weapon3ID)]
        newWeapon4ID = CONFIG.WEAPON_REGISTER[int(self.weapon4ID)]

        newWeaponIDList = [newWeapon1ID, newWeapon2ID, newWeapon3ID, newWeapon4ID]

        for weapon in newWeaponIDList:
            if weapon == 'SlugGun':
                newWeapon = weaponDefList['SlugGun'].SlugGun()
            elif weapon == 'MachineGun':
                newWeapon = weaponDefList['MachineGun'].MachineGun()
            elif weapon == 'Mortar':
                newWeapon = weaponDefList['Mortar'].Mortar()

            elif weapon == 'None' or weapon == None:
                newWeapon = None

            if weapon != None:
                newWeapon.owner = self
                newWeapon.console = self.console
            self.weapons.append(newWeapon)



    # handles what the mech does when it has a chance to attack.
    def attack(self, gameState, target, weapon, enemyList):
        '''
        deal attack damage to one target
        '''

        # if the weapon is not able to rapid fire, take one shot
        if weapon.rate == 1:
            didFire, gameState = weapon.fire(gameState, target)
            # if the weapon has 'splash' damage (ie, it is an explosion), deal damage to other mechs too
            if weapon.splash != 0 and didFire:
                i = weapon.splash
                while i > 0:
                    newTarget = self.selectTarget(enemyList)
                    if newTarget == target:
                        continue
                    didFire, gameState = weapon.fire(gameState, newTarget, splashShot=True)
                    i -= 1


        # the weapon is able to rapid fire.  Handle each shot the weapon takes this round.
        else:
            i = weapon.rate
            while i > 0:
                newTarget = self.selectTarget(enemyList)
                if i == 1:
                    didFire, gameState = weapon.fire(gameState, newTarget)
                else:
                    didFire, gameState = weapon.fire(gameState, newTarget, rateShot=True)
                i -= 1

            # for each shot, if the shot was an explosion, deal damage to other mechs too.
            if weapon.splash != 0:
                i = weapon.splash
                while i > 0:
                    newTarget = self.selectTarget(enemyList)
                    if newTarget == target:
                        continue
                    didFire, gameState = weapon.fire(gameState, newTarget, splashShot=True)
                    i -= 1

        # if the weapon fired this turn, we add heat to it, and remove some ammo.  If the mech is overheating, we then 
        # force it to spend the next round it has just cooling off.
        if didFire:
            self.heat += weapon.heatRate
            weapon.ammo -= 1
            if self.coolOff == True:
                self.coolOff = False

        # return information about whether the game has ended.  If this shot killed off the last mech on the other team, the game will end here.
        return gameState



    # below are instructions telling the computer how to select which enemy to fire at.  Essentially, it is totally random who you shoot at with each shot.
    def selectTarget(self, enemyList):
        '''
        choose one opposing mech, and set it as the target for this round
        '''
        choice = random.randint(0, len(enemyList) - 1)
        enemy = enemyList[choice]

        return enemy


    # This describes what happens when a mech has taken more damage than it has available.  Basically, this describes how a mech 'dies'.
    def death(self, team):
        '''
        runs when an avatar dies
        '''
        # remove the mech from the team it is on.
        team.remove(self)
        # display a message in the console about the mech's death
        self.console.messageList.insert(0, "[" + self.team + "] " + str(self.name).capitalize() + " perished. (" + str(self.deathBlow) + " damage this turn.)")
        return team




# This describes the stats a weapon has, and how it handles firing at an enemy
class Weapon():

    # set up the initial stats of the weapon.
    def __init__(self, owner, name, firepower, tracking, splash, ammo, rate, console=None):
        self.owner = owner
        self.name = name
        self.firepower = firepower
        self.tracking = tracking
        self.splash = splash
        self.ammo = ammo
        self.ammoCapacity = ammo
        self.rate = rate
        self.console = console

        self.heatRate = self.firepower + (self.splash*(self.firepower*self.rate)) + (self.firepower * self.rate)
        self.speedPenalty = (self.firepower*2) + self.tracking + self.splash + self.ammo + (self.rate * self.firepower)


    # This describes what happens with a single shot by the weapon
    def fire(self, gameState, target, rateShot=False, splashShot=False):
        '''
        handles one shot of the weapon at the given target
        '''

        # you can safely ignore this.  Animation is not yet in the game.
        if gameState == 'animation':        # the animation has not finished from the last shot.
            self.animate()
            return False, gameState

        # if the mech needs to cool off, display a message about it in the console.
        if self.owner.coolOff == True:
            messageString =  str(self.owner.name).capitalize() + " is cooling off."
            self.console.messageList.insert(0,messageString)
            return False, gameState

        # If a mech is so slow it *cannot* evade shots, then it will take extra damage each time it is hit. This represents the ability to take
        # your time aiming in order to hit a particularly vulnerable spot on the mech.
        targetDamageMod = 0 - target.evasion
        if targetDamageMod < 0:
            targetDamageMod = 0

        # If the mech is overheating, spend this shot cooling off instead of firing.
        if self.owner.heat >= CONFIG.HEAT_LIMIT:
            self.coolDown()
            messageString =  str(self.owner.name).capitalize() + " is cooling off."
            self.console.messageList.insert(0,messageString)
            return False, gameState

        # if the weapon is out of ammo, spend this shot reloading instead of firing.
        if self.ammo <= 0:
            if rateShot == False:
                self.reload()
                messageString =  str(self.owner.name).capitalize() + " is reloading the " + str(self.name) + "."
            elif rateShot:
                messageString = str(self.owner.name).capitalize() + "'s " + str(self.name) + " is out of ammo!"
            self.console.messageList.insert(0,messageString)
            return False, gameState

        # improve the weapon's chances to hit the enemy if it has more than 0 in the 'tracking' stat
        hitBonus = 0
        hitBonus = hitBonus + (self.tracking * 2) - self.rate

        # roll a 20-sided die to see if the weapon hit the target
        hitRoll = random.randint(1,20)
        if splashShot == False:
            # the weapon hit!  Display a message in the console, and deal the target some damage
            if hitRoll > target.evasion or hitRoll == 20:
                target.damageTaken += self.firepower + targetDamageMod
                messageString =  str(self.owner.name).capitalize() + " fires the " + self.name + " at " + str(target.name).capitalize() + " for " + str(self.firepower + targetDamageMod) + " damage. (" + str(hitRoll) + ":" + str(target.evasion) + ")"
                self.console.messageList.insert(0, messageString)
                return True, gameState
            # the weapon missed.  Display a message in the console about it.
            else:
                messageString = str(self.owner.name).capitalize() + " missed " + str(target.name).capitalize() + " with the " + self.name + "! (" + str(hitRoll) + ":" + str(target.evasion) + ")"
                self.console.messageList.insert(0, messageString)
                return True, gameState

        # if the weapon has 'splash' (ie, it is an explosive weapon), deal some damage to mechs other than the target
        else:
            if hitRoll > 10:
                target.damageTaken += 1
                messageString = str(self.owner.name).capitalize() + " catches " + str(target.name).capitalize() + " in the explosion from the " + self.name + " for " + str(1) + " damage."
                self.console.messageList.insert(0, messageString)
                return True, gameState
            else:
                return False, gameState



    # when the weapon is out of ammo, this runs instead of taking a shot.  The weapon will have full ammo again.
    def reload(self):
        '''
        replenishes ammo at the cost of 1 turn doing nothing
        '''
        if self.ammo <= 0:
            self.ammo = self.ammoCapacity


    # if a mech is overheated, spend the round cooling off instead of shooting.  If the mech has no heat sinks, it will never cool down and will
    # eventually be forced to quit shooting in the battle!
    def coolDown(self):
        '''
        lowers the mech's heat by spending a turn doing nothing
        '''
        if self.owner.heat >= CONFIG.HEAT_LIMIT:
            self.owner.heat -= self.owner.heatSinks * 2

        self.owner.coolOff = False

        messageString =  str(self.owner.name).capitalize() + " is cooling off."
        self.console.messageList.append(messageString)


    # this can be ignored, as animation is not yet in the game.
    def animate(self):
        '''
        plays the weapon's animation when fired
        '''
        pass

