#classes
#class definitions

import random, time
import pygame
import fileLoader, IDs, CONFIG


pygame.init()



class Avatar():
    '''
    an avatar is a representation of a player.  It is constructed from data obtained from the RFID readers, and does the battling.
    '''
    def __init__(self, rfidString, team, console):
        self.FileLoader = fileLoader.FileLoader()

        self.team = team
        self.console = console
        self.definition = rfidString
        self.ID = self.definition[0] + self.definition[1]
        self.name = IDs.playerList[int(self.ID)-1][0]

        self.tinyImage = None
        if IDs.playerList[int(self.ID)-1][1] != None:
            self.image = IDs.playerList[int(self.ID)-1][1]
        else:
            self.image = None

        if self.image != None:
            #print "WIN"
            self.loadImage()
            #print self.tinyImage

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


    @property
    def cooling(self):
        cooling = self.heatSinks + 1
        return cooling


    @property
    def evasion(self):
        evasion = CONFIG.BASE_EVASION
        if self.armor != 0:
            evasion -= (2*self.armor)
        # if self.targeting != 0:
        #     evasion -= self.targeting
        if self.heatSinks != 0:
            evasion -= self.heatSinks
        for weapon in self.weapons:
            if weapon != None:
                evasion -= weapon.speedPenalty

        # if evasion < 0:
        #     evasion = 0
        return evasion


    def loadImage(self):
        '''
        loads a custom image as defined in IDs.py
        '''
        imagePath = self.image
        self.image = pygame.image.load(CONFIG.IMAGE_PATH + imagePath)
        self.image.convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.tinyImage = pygame.transform.scale(self.image, (32, 32))


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


    def attack(self, gameState, target, weapon, enemyList):
        '''
        deal attack damage to one target
        '''
        if weapon.rate == 1:
            didFire, gameState = weapon.fire(gameState, target)
            if weapon.splash != 0 and didFire:
                i = weapon.splash
                while i > 0:
                    newTarget = self.selectTarget(enemyList)
                    if newTarget == target:
                        continue
                    didFire, gameState = weapon.fire(gameState, newTarget, splashShot=True)
                    i -= 1
        else:
            i = weapon.rate
            while i > 0:
                newTarget = self.selectTarget(enemyList)
                if i == 1:
                    didFire, gameState = weapon.fire(gameState, newTarget)
                else:
                    didFire, gameState = weapon.fire(gameState, newTarget, rateShot=True)
                i -= 1

            if weapon.splash != 0:
                i = weapon.splash
                while i > 0:
                    newTarget = self.selectTarget(enemyList)
                    if newTarget == target:
                        continue
                    didFire, gameState = weapon.fire(gameState, newTarget, splashShot=True)
                    i -= 1

        if didFire:
            self.heat += weapon.heatRate
            #print self.ID, self.heat
            weapon.ammo -= 1
            if self.coolOff == True:
                self.coolOff = False

        return gameState


    def selectTarget(self, enemyList):
        '''
        choose one opposing mech, and set it as the target for this turn
        '''
        # currentTimeSeed = time.time()
        # random.seed(currentTimeSeed)
        choice = random.randint(0, len(enemyList) - 1)
        enemy = enemyList[choice]

        #print self, enemy

        return enemy


    def death(self, team):
        '''
        runs when an avatar dies
        '''
        team.remove(self)
        #print "[" + self.team + "] " + self.ID + " perished. "
        self.console.messageList.insert(0, "[" + self.team + "] " + str(self.name).capitalize() + " perished. (" + str(self.deathBlow) + " damage this turn.)")
        return team



class Weapon():
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


    def fire(self, gameState, target, rateShot=False, splashShot=False):
        '''
        handles one shot of the weapon at the given target
        '''
        if gameState == 'animation':        # the animation has not finished from the last shot.
            self.animate()
            return False, gameState

        if self.owner.coolOff == True:
            messageString =  str(self.owner.name).capitalize() + " is cooling off."
            self.console.messageList.insert(0,messageString)
            return False, gameState

        targetDamageMod = 0 - target.evasion
        if targetDamageMod < 0:
            targetDamageMod = 0

        if self.owner.heat >= CONFIG.HEAT_LIMIT:
            self.coolDown()
            messageString =  str(self.owner.name).capitalize() + " is cooling off."
            self.console.messageList.insert(0,messageString)
            return False, gameState

        if self.ammo <= 0:
            if rateShot == False:
                self.reload()
                messageString =  str(self.owner.name).capitalize() + " is reloading the " + str(self.name) + "."
            elif rateShot:
                messageString = str(self.owner.name).capitalize() + "'s " + str(self.name) + " is out of ammo!"
            self.console.messageList.insert(0,messageString)
            return False, gameState

        hitBonus = 0
        hitBonus = hitBonus + (self.tracking * 2) - self.rate

        hitRoll = random.randint(1,20)
        if splashShot == False:
            if hitRoll > target.evasion or hitRoll == 20:
                target.damageTaken += self.firepower + targetDamageMod
                messageString =  str(self.owner.name).capitalize() + " fires the " + self.name + " at " + str(target.name).capitalize() + " for " + str(self.firepower + targetDamageMod) + " damage. (" + str(hitRoll) + ":" + str(target.evasion) + ")"
                self.console.messageList.insert(0, messageString)
                return True, gameState
            else:
                messageString = str(self.owner.name).capitalize() + " missed " + str(target.name).capitalize() + " with the " + self.name + "! (" + str(hitRoll) + ":" + str(target.evasion) + ")"
                self.console.messageList.insert(0, messageString)
                return True, gameState
        else:
            if hitRoll > 10:
                target.damageTaken += 1
                messageString = str(self.owner.name).capitalize() + " catches " + str(target.name).capitalize() + " in the explosion from the " + self.name + " for " + str(1) + " damage."
                self.console.messageList.insert(0, messageString)
                return True, gameState
            else:
                return False, gameState


    def reload(self):
        '''
        replenishes ammo at the cost of 1 turn doing nothing
        '''
        if self.ammo <= 0:
            self.ammo = self.ammoCapacity


    def coolDown(self):
        '''
        lowers the mech's heat by spending a turn doing nothing
        '''
        if self.owner.heat >= CONFIG.HEAT_LIMIT:
            self.owner.heat -= self.owner.heatSinks * 2

        self.owner.coolOff = False

        messageString =  str(self.owner.name).capitalize() + " is cooling off."
        self.console.messageList.append(messageString)


    def animate(self):
        '''
        plays the weapon's animation when fired
        '''
        pass

